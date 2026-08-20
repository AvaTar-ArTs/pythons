#!/usr/bin/env python3
"""
NFT Creator - Automated NFT generation and minting
Creates NFTs from AI-generated content and manages collections
"""

import os
import json
import hashlib
import requests
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
from PIL import Image
import web3
from web3 import Web3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NFTMetadata:
    """NFT metadata structure"""
    name: str
    description: str
    image: str
    external_url: str
    attributes: List[Dict[str, Any]]
    background_color: str
    animation_url: Optional[str] = None
    youtube_url: Optional[str] = None

@dataclass
class NFTCollection:
    """NFT collection structure"""
    name: str
    description: str
    image: str
    external_link: str
    seller_fee_basis_points: int
    fee_recipient: str
    total_supply: int
    created_at: str

class NFTCreator:
    """NFT creation and management system"""
    
    def __init__(self, config_path: str = "config/nft_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.web3 = self._init_web3()
        self.collections = {}
        
    def _load_config(self) -> Dict[str, Any]:
        """Load NFT configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default NFT configuration"""
        return {
            "networks": {
                "ethereum": {
                    "rpc_url": "https://mainnet.infura.io/v3/YOUR_PROJECT_ID",
                    "chain_id": 1,
                    "contract_address": "",
                    "private_key": ""
                },
                "polygon": {
                    "rpc_url": "https://polygon-rpc.com",
                    "chain_id": 137,
                    "contract_address": "",
                    "private_key": ""
                }
            },
            "ipfs": {
                "gateway": "https://ipfs.io/ipfs/",
                "pin_service": "pinata",
                "api_key": "",
                "secret_key": ""
            },
            "opensea": {
                "api_key": "",
                "collection_slug": ""
            }
        }
    
    def _init_web3(self) -> Web3:
        """Initialize Web3 connection"""
        try:
            network_config = self.config["networks"]["ethereum"]
            w3 = Web3(Web3.HTTPProvider(network_config["rpc_url"]))
            if w3.is_connected():
                logger.info("Connected to Ethereum network")
                return w3
            else:
                logger.error("Failed to connect to Ethereum network")
                return None
        except Exception as e:
            logger.error(f"Web3 initialization failed: {e}")
            return None
    
    def create_nft_metadata(self, 
                          image_path: str, 
                          name: str, 
                          description: str,
                          attributes: List[Dict[str, Any]] = None,
                          collection_name: str = "AI Generated Art") -> NFTMetadata:
        """Create NFT metadata from image and details"""
        try:
            # Upload image to IPFS
            image_url = self._upload_to_ipfs(image_path)
            
            # Generate unique token ID
            token_id = self._generate_token_id(image_path, name)
            
            # Create metadata
            metadata = NFTMetadata(
                name=name,
                description=description,
                image=image_url,
                external_url=f"https://opensea.io/assets/{self.config['opensea']['collection_slug']}/{token_id}",
                attributes=attributes or [],
                background_color="000000",
                animation_url=None,
                youtube_url=None
            )
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to create NFT metadata: {e}")
            return None
    
    def _upload_to_ipfs(self, file_path: str) -> str:
        """Upload file to IPFS and return hash"""
        try:
            if self.config["ipfs"]["pin_service"] == "pinata":
                return self._upload_to_pinata(file_path)
            else:
                return self._upload_to_local_ipfs(file_path)
        except Exception as e:
            logger.error(f"IPFS upload failed: {e}")
            return ""
    
    def _upload_to_pinata(self, file_path: str) -> str:
        """Upload file to Pinata IPFS service"""
        try:
            pinata_api_key = self.config["ipfs"]["api_key"]
            pinata_secret = self.config["ipfs"]["secret_key"]
            
            headers = {
                "pinata_api_key": pinata_api_key,
                "pinata_secret_api_key": pinata_secret
            }
            
            with open(file_path, 'rb') as f:
                files = {"file": f}
                response = requests.post(
                    "https://api.pinata.cloud/pinning/pinFileToIPFS",
                    headers=headers,
                    files=files
                )
            
            if response.status_code == 200:
                result = response.json()
                ipfs_hash = result["IpfsHash"]
                return f"https://ipfs.io/ipfs/{ipfs_hash}"
            else:
                logger.error(f"Pinata upload failed: {response.status_code}")
                return ""
                
        except Exception as e:
            logger.error(f"Pinata upload error: {e}")
            return ""
    
    def _generate_token_id(self, image_path: str, name: str) -> int:
        """Generate unique token ID"""
        content = f"{image_path}{name}{datetime.now().isoformat()}"
        hash_object = hashlib.sha256(content.encode())
        return int(hash_object.hexdigest()[:8], 16)
    
    def create_nft_collection(self, 
                            collection_name: str,
                            description: str,
                            image_path: str,
                            seller_fee: int = 250) -> NFTCollection:
        """Create a new NFT collection"""
        try:
            # Upload collection image to IPFS
            collection_image_url = self._upload_to_ipFS(image_path)
            
            collection = NFTCollection(
                name=collection_name,
                description=description,
                image=collection_image_url,
                external_link="https://opensea.io/collection/" + collection_name.lower().replace(" ", "-"),
                seller_fee_basis_points=seller_fee,
                fee_recipient=self.config["networks"]["ethereum"]["contract_address"],
                total_supply=0,
                created_at=datetime.now().isoformat()
            )
            
            self.collections[collection_name] = collection
            return collection
            
        except Exception as e:
            logger.error(f"Failed to create NFT collection: {e}")
            return None
    
    def batch_create_nfts(self, 
                         image_directory: str,
                         collection_name: str,
                         base_description: str,
                         attributes_template: List[Dict[str, Any]] = None) -> List[str]:
        """Create multiple NFTs from directory of images"""
        try:
            nft_hashes = []
            
            # Get all image files
            image_files = [f for f in os.listdir(image_directory) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
            
            for i, image_file in enumerate(image_files):
                image_path = os.path.join(image_directory, image_file)
                
                # Generate name and description
                name = f"{collection_name} #{i+1}"
                description = f"{base_description} - Part of the {collection_name} collection"
                
                # Create attributes
                attributes = self._generate_attributes(attributes_template, image_file)
                
                # Create NFT metadata
                metadata = self.create_nft_metadata(
                    image_path=image_path,
                    name=name,
                    description=description,
                    attributes=attributes,
                    collection_name=collection_name
                )
                
                if metadata:
                    # Save metadata to file
                    metadata_path = f"output/nfts/{collection_name}_{i+1}_metadata.json"
                    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
                    
                    with open(metadata_path, 'w') as f:
                        json.dump(metadata.__dict__, f, indent=2)
                    
                    nft_hashes.append(metadata_path)
                    logger.info(f"Created NFT metadata for {name}")
            
            return nft_hashes
            
        except Exception as e:
            logger.error(f"Batch NFT creation failed: {e}")
            return []
    
    def _generate_attributes(self, template: List[Dict[str, Any]], image_file: str) -> List[Dict[str, Any]]:
        """Generate NFT attributes from template"""
        if not template:
            return [
                {"trait_type": "Type", "value": "AI Generated"},
                {"trait_type": "Rarity", "value": "Common"},
                {"trait_type": "Artist", "value": "AI Studio"}
            ]
        
        attributes = []
        for attr in template:
            if attr["type"] == "static":
                attributes.append({
                    "trait_type": attr["name"],
                    "value": attr["value"]
                })
            elif attr["type"] == "random":
                import random
                value = random.choice(attr["options"])
                attributes.append({
                    "trait_type": attr["name"],
                    "value": value
                })
            elif attr["type"] == "filename":
                value = os.path.splitext(image_file)[0]
                attributes.append({
                    "trait_type": attr["name"],
                    "value": value
                })
        
        return attributes
    
    def sync_to_opensea(self, collection_name: str) -> bool:
        """Sync NFT collection to OpenSea"""
        try:
            collection = self.collections.get(collection_name)
            if not collection:
                logger.error(f"Collection {collection_name} not found")
                return False
            
            # OpenSea API integration would go here
            # This is a placeholder for the actual implementation
            logger.info(f"Syncing collection {collection_name} to OpenSea...")
            
            # In a real implementation, you would:
            # 1. Create collection on OpenSea
            # 2. Upload metadata
            # 3. Set collection properties
            # 4. Verify sync status
            
            return True
            
        except Exception as e:
            logger.error(f"OpenSea sync failed: {e}")
            return False
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            collection = self.collections.get(collection_name)
            if not collection:
                return {}
            
            # Get NFT files in collection
            nft_files = [f for f in os.listdir("output/nfts") 
                        if f.startswith(collection_name)]
            
            return {
                "collection_name": collection_name,
                "total_nfts": len(nft_files),
                "created_at": collection.created_at,
                "external_url": collection.external_link,
                "seller_fee": collection.seller_fee_basis_points
            }
            
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {}

# Example usage
def main():
    """Example usage of NFT Creator"""
    creator = NFTCreator()
    
    # Create a collection
    collection = creator.create_nft_collection(
        collection_name="AI Digital Art",
        description="Unique AI-generated digital art pieces",
        image_path="assets/collection_banner.png"
    )
    
    if collection:
        print(f"Created collection: {collection.name}")
        
        # Create NFTs from images
        nft_hashes = creator.batch_create_nfts(
            image_directory="input/images",
            collection_name="AI Digital Art",
            base_description="Beautiful AI-generated artwork",
            attributes_template=[
                {"type": "static", "name": "Artist", "value": "AI Studio"},
                {"type": "random", "name": "Style", "options": ["Abstract", "Realistic", "Fantasy"]},
                {"type": "random", "name": "Color", "options": ["Vibrant", "Monochrome", "Pastel"]}
            ]
        )
        
        print(f"Created {len(nft_hashes)} NFTs")
        
        # Sync to OpenSea
        if creator.sync_to_opensea("AI Digital Art"):
            print("Collection synced to OpenSea")

if __name__ == "__main__":
    main()