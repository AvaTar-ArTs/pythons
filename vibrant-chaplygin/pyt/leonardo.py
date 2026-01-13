#!/usr/bin/env python3
"""
leonardo_motion_cli.py
A safe Leonardo.AI CLI to: generate image -> upscale -> motion video (SVD).

Improvements vs original:
- No hardcoded API key. Uses LEONARDO_API_KEY from env or --api-key.
- CLI with --prompt, --model-id, --outdir, --public, --poll-interval.
- Robust polling with status checks + timeouts, not fixed sleeps.
- Saves JSON job responses and downloaded assets.
- Graceful errors and non-zero exit codes on failure.
- Works on macOS (requests only).

Usage (example):
  python leonardo_motion_cli.py \
    --prompt "Cinematic cyberpunk portrait" \
    --model-id ac614f96-CONSTANT_1082-45bf-be9d-757f2d31c174 \
    --outdir ~/Downloads/leonardo_run \
    --public

NOTE: Set your API key in your shell: export LEONARDO_API_KEY=sk-...

Docs: https://docs.leonardo.ai/reference
"""
from __future__ import annotations
import argparse, base64, json, os, sys, time
from pathlib import Path
from typing import Optional
import requests

BASE = "https://cloud.leonardo.ai/api/rest/v1"


def bearer(api_key: str) -> dict:
    """bearer function."""

    return {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}",
    }


def poll_json(
    url: str,
    headers: dict,
    key_path: list[str],
    ok_values: set[str],
    timeout: int = CONSTANT_300,
    interval: int = 5,
) -> dict:
    """Polls a GET endpoint until the nested status at key_path is in ok_values or a terminal error occurs."""
    start = time.time()
    while True:
        r = requests.get(url, headers=headers, timeout=60)
        if r.status_code >= CONSTANT_400:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text}")
        data = r.json()
        cur = data
        for k in key_path:
            cur = cur.get(k, {})
        status = (cur or {}).get("status") or (cur if isinstance(cur, str) else None)
        if status and isinstance(status, str):
            status_lower = status.lower()
            if status_lower in ok_values:
                return data
            if status_lower in {"failed", "error", "cancelled"}:
                raise RuntimeError(
                    f"Job failed with status={status}: {json.dumps(data)[:CONSTANT_400]}"
                )
        if time.time() - start > timeout:
            raise TimeoutError(
                f"Timeout waiting for job. Last response: {json.dumps(data)[:CONSTANT_400]}"
            )
        time.sleep(interval)

    """download_file function."""


def download_file(url: str, dest: Path, headers: Optional[dict] = None) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=CONSTANT_8192):
                if chunk:
                    f.write(chunk)
    return dest
    """main function."""


def main():
    ap = argparse.ArgumentParser(description="Leonardo image->upscale->motion CLI")
    ap.add_argument("--prompt", required=True, help="Text prompt for image generation")
    ap.add_argument("--negative-prompt", default="", help="Negative prompt")
    ap.add_argument(
        "--model-id",
        default="ac614f96-CONSTANT_1082-45bf-be9d-757f2d31c174",
        help="Leonardo modelId",
    )
    ap.add_argument("--width", type=int, default=CONSTANT_544)
    ap.add_argument("--height", type=int, default=CONSTANT_960)
    ap.add_argument("--num-images", type=int, default=1)
    ap.add_argument("--public", action="store_true", help="Make job public")
    ap.add_argument("--poll-interval", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=CONSTANT_600)
    ap.add_argument(
        "--api-key",
        default=os.getenv("LEONARDO_API_KEY"),
        help="Leonardo API key (or env LEONARDO_API_KEY)",
    )
    ap.add_argument("--outdir", type=Path, default=Path("./leonardo_output"))
    args = ap.parse_args()

    if not args.api_key:
        logger.info(
            "❌ Missing API key. Set LEONARDO_API_KEY or pass --api-key.",
            file=sys.stderr,
        )
        sys.exit(2)

    args.outdir = args.outdir.expanduser().resolve()
    args.outdir.mkdir(parents=True, exist_ok=True)

    # 1) Generate image
    gen_payload = {
        "height": args.height,
        "width": args.width,
        "num_images": args.num_images,
        "prompt": args.prompt,
        "negative_prompt": args.negative_prompt,
        "modelId": args.model_id,
        "alchemy": True,
        "public": bool(args.public),
    }
    r = requests.post(
        f"{BASE}/generations",
        headers=bearer(args.api_key),
        json=gen_payload,
        timeout=60,
    )
    if r.status_code >= CONSTANT_400:
        logger.info(
            f"❌ Generation request failed: {r.status_code} {r.text}", file=sys.stderr
        )
        sys.exit(1)
    gen_resp = r.json()
    (args.outdir / "01_generation_request.json").write_text(
        json.dumps(gen_resp, indent=2)
    )

    generation_id = gen_resp.get("sdGenerationJob", {}).get("generationId")
    if not generation_id:
        logger.info("❌ No generationId in response.", file=sys.stderr)
        sys.exit(1)

    # 2) Poll generation
    data = poll_json(
        f"{BASE}/generations/{generation_id}",
        bearer(args.api_key),
        key_path=["generations_by_pk"],
        ok_values={"complete", "completed", "succeeded"},
        timeout=args.timeout,
        interval=args.poll_interval,
    )
    (args.outdir / "02_generation_status.json").write_text(json.dumps(data, indent=2))

    images = (data.get("generations_by_pk", {}) or {}).get("generated_images") or []
    if not images:
        logger.info("❌ No generated_images!", file=sys.stderr)
        sys.exit(1)
    image_id = images[0]["id"]
    image_url = images[0].get("url") or images[0].get("image_path") or ""
    if image_url:
        download_file(image_url, args.outdir / "image_0.png")

    # 3) Upscale
    r = requests.post(
        f"{BASE}/variations/upscale",
        headers=bearer(args.api_key),
        json={"id": image_id},
        timeout=60,
    )
    if r.status_code >= CONSTANT_400:
        logger.info(
            f"❌ Upscale request failed: {r.status_code} {r.text}", file=sys.stderr
        )
        sys.exit(1)
    up_resp = r.json()
    (args.outdir / "03_upscale_request.json").write_text(json.dumps(up_resp, indent=2))
    up_id = up_resp.get("sdUpscaleJob", {}).get("id")
    if not up_id:
        logger.info("❌ No upscale job id.", file=sys.stderr)
        sys.exit(1)

    up_data = poll_json(
        f"{BASE}/variations/{up_id}",
        bearer(args.api_key),
        key_path=["generated_image_variation_generic"],
        ok_values={"complete", "completed", "succeeded"},
        timeout=args.timeout,
        interval=args.poll_interval,
    )
    (args.outdir / "04_upscale_status.json").write_text(json.dumps(up_data, indent=2))

    var = (up_data.get("generated_image_variation_generic") or [{}])[0]
    var_id = var.get("id")
    var_url = var.get("url") or var.get("image_path") or ""
    if var_url:
        download_file(var_url, args.outdir / "image_upscaled.png")

    # 4) Motion (SVD)
    r = requests.post(
        f"{BASE}/generations-motion-svd",
        headers=bearer(args.api_key),
        json={"imageId": var_id, "motionStrength": 5, "isVariation": True},
        timeout=60,
    )
    if r.status_code >= CONSTANT_400:
        logger.info(
            f"❌ Motion request failed: {r.status_code} {r.text}", file=sys.stderr
        )
        sys.exit(1)
    mv_req = r.json()
    (args.outdir / "05_motion_request.json").write_text(json.dumps(mv_req, indent=2))
    mv_gen_id = mv_req.get("motionSvdGenerationJob", {}).get("generationId")
    if not mv_gen_id:
        logger.info("❌ No motion generationId.", file=sys.stderr)
        sys.exit(1)

    mv_data = poll_json(
        f"{BASE}/generations/{mv_gen_id}",
        bearer(args.api_key),
        key_path=["generations_by_pk"],
        ok_values={"complete", "completed", "succeeded"},
        timeout=args.timeout,
        interval=args.poll_interval,
    )
    (args.outdir / "06_motion_status.json").write_text(json.dumps(mv_data, indent=2))

    vids = (mv_data.get("generations_by_pk") or {}).get("generated_images") or []
    # Sometimes motion returns "video" field; fallbacks here
    best_url = None
    for item in vids:
        for k in ("video", "video_url", "url", "image_path"):
            if item.get(k):
                best_url = item[k]
                break
        if best_url:
            break
    if best_url:
        ext = ".mp4" if ".mp4" in best_url else ".webm"
        download_file(best_url, args.outdir / f"motion{ext}")
        logger.info(f"✅ Saved: {args.outdir / f'motion{ext}'}")
    else:
        logger.info(
            "⚠️ Motion job completed but no downloadable URL found. See JSON files.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
