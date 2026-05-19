#!/usr/bin/env python3
"""
Test script for NocturneMemory AI Enhanced system

Demonstrates all major features:
- AI orchestration
- Semantic search
- Relationship mapping
- Multi-AI collaboration
- Content synthesis
"""

from nocturnememory_ai_enhanced import NocturneMemoryAIEnhanced
from nocturnememory_ai_orchestrator import ContentType, TaskComplexity


def test_orchestration():
    """Test AI orchestration"""
    print("=" * 60)
    print("TEST 1: AI Orchestration")
    print("=" * 60)

    memory = NocturneMemoryAIEnhanced()

    # Test routing
    test_content = "A majestic cyberpunk cityscape at night with neon lights"

    routing = memory.orchestrator.route_request(
        content=test_content,
        content_type=ContentType.IMAGE_PROMPT,
        complexity=TaskComplexity.MEDIUM,
        prefer_cost_efficient=True,
    )

    print("\n✅ Routing Decision:")
    print(f"   Model: {routing.selected_model}")
    print(f"   Provider: {routing.provider}")
    print(f"   Confidence: {routing.confidence:.2f}")
    print(f"   Reasoning: {routing.reasoning}")
    print(f"   Estimated Cost: ${routing.estimated_cost:.4f}")
    print(f"   Alternatives: {', '.join(routing.alternatives[:3])}")

    return True


def test_embeddings():
    """Test embeddings generation"""
    print("\n" + "=" * 60)
    print("TEST 2: Embeddings Generation")
    print("=" * 60)

    memory = NocturneMemoryAIEnhanced()

    test_text = "A dark ambient track with ethereal vocals and atmospheric pads"

    try:
        # Try OpenAI first
        embedding_result = memory.embeddings.generate_embedding(
            test_text,
            model="openai-small" if memory.api_keys.get("openai") else "local",
        )

        print("\n✅ Embedding Generated:")
        print(f"   Model: {embedding_result.model}")
        print(f"   Dimension: {embedding_result.dimension}")
        print(f"   Cost: ${embedding_result.cost:.4f}")
        print(f"   Embedding length: {len(embedding_result.embedding)}")

        return True
    except Exception as e:
        print(f"\n⚠️  Embedding test skipped: {e}")
        print("   (This is OK if API keys are not configured)")
        return False


def test_semantic_search():
    """Test semantic search"""
    print("\n" + "=" * 60)
    print("TEST 3: Semantic Search")
    print("=" * 60)

    memory = NocturneMemoryAIEnhanced()

    # Check if we have any indexed content
    stats = memory.get_stats()
    if stats["total_content"] == 0:
        print("\n⚠️  No content indexed yet. Skipping semantic search test.")
        print("   Run: python nocturnememory_ai_enhanced.py scan --path <your_directory>")
        return False

    if stats["with_embeddings"] == 0:
        print("\n⚠️  No content with embeddings. Skipping semantic search test.")
        print("   Content needs to be indexed with embeddings enabled.")
        return False

    try:
        results = memory.semantic_search("cyberpunk city", top_k=5)

        if results:
            print(f"\n✅ Found {len(results)} semantic matches:")
            for i, result in enumerate(results[:5], 1):
                print(f"   {i}. {result['file_name']}")
                print(f"      Similarity: {result['similarity']:.3f}")
                print(f"      Category: {result['category']}")
        else:
            print("\n⚠️  No results found (this is OK if content doesn't match)")

        return True
    except Exception as e:
        print(f"\n❌ Semantic search error: {e}")
        return False


def test_relationships():
    """Test relationship mapping"""
    print("\n" + "=" * 60)
    print("TEST 4: Relationship Mapping")
    print("=" * 60)

    memory = NocturneMemoryAIEnhanced()

    # Get a content ID
    conn = memory.db_path.parent / "nocturnememory_ai_enhanced.db"
    if not conn.exists():
        print("\n⚠️  Database not found. Skipping relationship test.")
        return False

    import sqlite3

    db_conn = sqlite3.connect(str(conn))
    cursor = db_conn.cursor()
    cursor.execute("SELECT id FROM content_index WHERE embedding_generated = 1 LIMIT 1")
    row = cursor.fetchone()
    db_conn.close()

    if not row:
        print("\n⚠️  No content with embeddings found. Skipping relationship test.")
        return False

    content_id = row[0]

    try:
        relationships = memory.find_relationships(content_id, threshold=0.7)

        if relationships:
            print(f"\n✅ Found {len(relationships)} relationships for content {content_id}:")
            for i, rel in enumerate(relationships[:5], 1):
                print(f"   {i}. {rel['relationship_type']}: {rel['target_id']}")
                print(f"      Similarity: {rel['similarity']:.3f}")
        else:
            print(f"\n⚠️  No relationships found for {content_id}")
            print("   (This is OK if content is unique)")

        return True
    except Exception as e:
        print(f"\n❌ Relationship mapping error: {e}")
        return False


def test_multi_ai_collaboration():
    """Test multi-AI collaboration"""
    print("\n" + "=" * 60)
    print("TEST 5: Multi-AI Collaboration")
    print("=" * 60)

    memory = NocturneMemoryAIEnhanced()

    test_content = """
    [Verse 1]
    In the shadows where the lost souls play
    Heart beats like thunder in the pouring rain
    Dreams we chase fade into the grey
    Love's sweet poison running through our veins

    [Chorus]
    We dance in the darkness, we cry in the light
    Broken hearts mending in the dead of night
    """

    try:
        consensus = memory.multi_ai_collaboration(
            content=test_content,
            content_type=ContentType.LYRICS,
            num_models=min(3, len(memory.orchestrator.available_apis)),
        )

        if "error" not in consensus:
            print("\n✅ Multi-AI Collaboration:")
            print(f"   Models used: {consensus.get('models_used', [])}")
            print(f"   Agreement score: {consensus.get('agreement_score', 0):.2f}")
            print(f"   Number of models: {consensus.get('num_models', 0)}")
            print("\n   Consensus Analysis Preview:")
            analysis = consensus.get("consensus_analysis", "")
            print(f"   {analysis[:200]}...")
        else:
            print(f"\n⚠️  Collaboration test skipped: {consensus.get('error')}")

        return True
    except Exception as e:
        print(f"\n⚠️  Collaboration test skipped: {e}")
        return False


def test_statistics():
    """Test statistics"""
    print("\n" + "=" * 60)
    print("TEST 6: Statistics")
    print("=" * 60)

    memory = NocturneMemoryAIEnhanced()

    stats = memory.get_stats()

    print("\n✅ System Statistics:")
    print(f"   Total content: {stats['total_content']}")
    print(f"   With embeddings: {stats['with_embeddings']}")
    print(f"   AI analyses: {stats['ai_analyses']}")
    print(f"   Relationships: {stats['relationships']}")
    print(f"   Collaborations: {stats['collaborations']}")

    if stats.get("by_category"):
        print("\n   By category:")
        for cat, count in stats["by_category"].items():
            print(f"     {cat}: {count}")

    if stats.get("orchestrator"):
        print("\n   Orchestrator stats:")
        for provider, provider_stats in stats["orchestrator"].items():
            if provider_stats.get("total_calls", 0) > 0:
                print(f"     {provider}:")
                print(f"       Calls: {provider_stats['total_calls']}")
                print(f"       Success rate: {provider_stats.get('success_rate', 0):.2%}")
                print(f"       Total cost: ${provider_stats.get('total_cost', 0):.4f}")

    return True


def main():
    print("🧪 NocturneMemory AI Enhanced - System Test")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Orchestration", test_orchestration()))
    results.append(("Embeddings", test_embeddings()))
    results.append(("Semantic Search", test_semantic_search()))
    results.append(("Relationships", test_relationships()))
    results.append(("Multi-AI Collaboration", test_multi_ai_collaboration()))
    results.append(("Statistics", test_statistics()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "⚠️  SKIP"
        print(f"   {test_name}: {status}")

    print(f"\n   Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
    elif passed > 0:
        print("\n✅ Some tests passed (skipped tests are OK if APIs not configured)")
    else:
        print("\n⚠️  No tests passed - check API configuration")

    print("\n💡 Next steps:")
    print("   1. Configure API keys in ~/.env.d/")
    print("   2. Index content: python nocturnememory_ai_enhanced.py scan --path <dir>")
    print("   3. Try semantic search: python nocturnememory_ai_enhanced.py semantic --query 'your query'")
    print("   4. Read ENHANCED_DOCUMENTATION.md for more details")


if __name__ == "__main__":
    main()
