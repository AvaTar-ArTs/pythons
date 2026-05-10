#!/usr/bin/env python3
"""Comprehensive Song Analysis Generator
Applies detailed narrative logic for visual storytelling and image generation
"""

import re
from dataclasses import dataclass


@dataclass
class SongAnalysis:
    """Data structure for comprehensive song analysis"""

    song_title: str
    genre_fusion: str
    primary_theme: str
    secondary_theme: str
    emotional_tone: str
    visual_style: str
    image_series_title: str
    core_narrative: str
    visual_metaphors: str
    emotional_journey: str
    character_archetype: str
    setting_atmosphere: str
    target_emotion: str
    core_message: str
    youtube_title: str
    seo_keywords: str
    digital_dive_instructions: str


class SongAnalysisGenerator:
    """Generates comprehensive song analysis using narrative logic"""

    def __init__(self):
        self.theme_keywords = {
            "nature": [
                "willow",
                "tree",
                "moonlight",
                "forest",
                "valley",
                "mist",
                "fireflies",
            ],
            "urban": [
                "alley",
                "graffiti",
                "neon",
                "concrete",
                "street",
                "city",
                "rebellion",
            ],
            "blues": [
                "guitar",
                "midnight",
                "soul",
                "healing",
                "music",
                "porch",
                "candlelight",
            ],
            "storm": [
                "lightning",
                "wind",
                "chaos",
                "power",
                "transformation",
                "phoenix",
                "tornado",
            ],
            "folk": [
                "traveler",
                "road",
                "journey",
                "crossroads",
                "map",
                "campfire",
                "wandering",
            ],
            "anti_romance": [
                "rubbish",
                "trash",
                "broken",
                "rebellion",
                "cynical",
                "punk",
                "defiant",
            ],
        }

        self.emotion_mapping = {
            "melancholic": ["sad", "lonely", "broken", "lost", "weary", "sorrow"],
            "defiant": [
                "angry",
                "rebellious",
                "fierce",
                "strong",
                "powerful",
                "unbreakable",
            ],
            "mystical": [
                "magical",
                "ethereal",
                "mysterious",
                "enchanting",
                "otherworldly",
            ],
            "intimate": ["close", "personal", "tender", "vulnerable", "gentle", "warm"],
            "chaotic": [
                "wild",
                "frenzied",
                "intense",
                "overwhelming",
                "turbulent",
                "explosive",
            ],
        }

        self.visual_styles = {
            "ethereal": "Moonlight Mystical",
            "urban": "Neon Graffiti Cyberpunk",
            "blues": "Moody Blue Tones Intimate",
            "storm": "Dramatic Stormy Epic",
            "folk": "Moody Atmospheric Mystical",
            "punk": "Neon Graffiti Cyberpunk",
        }

        self.character_archetypes = {
            "nature": "The Wounded Healer seeking solace in nature",
            "urban": "The Urban Rebel rejecting conventional love",
            "blues": "The Soulful Musician expressing deep emotion",
            "storm": "The Storm Warrior embracing inner power",
            "folk": "The Wandering Seeker on a quest for meaning",
            "anti_romance": "The Urban Rebel rejecting conventional love",
        }

    def analyze_lyrics(self, lyrics: str) -> dict[str, any]:
        """Analyze song lyrics to extract themes, emotions, and visual elements"""
        lyrics_lower = lyrics.lower()

        # Determine primary theme
        theme_scores = {}
        for theme, keywords in self.theme_keywords.items():
            score = sum(1 for keyword in keywords if keyword in lyrics_lower)
            theme_scores[theme] = score

        primary_theme = (
            max(theme_scores, key=theme_scores.get) if theme_scores else "folk"
        )

        # Determine emotional tone
        emotion_scores = {}
        for emotion, keywords in self.emotion_mapping.items():
            score = sum(1 for keyword in keywords if keyword in lyrics_lower)
            emotion_scores[emotion] = score

        emotional_tone = (
            max(emotion_scores, key=emotion_scores.get)
            if emotion_scores
            else "melancholic"
        )

        # Extract key phrases for visual metaphors
        visual_metaphors = self._extract_visual_metaphors(lyrics)

        # Generate narrative elements
        narrative_elements = self._generate_narrative_elements(
            primary_theme,
            emotional_tone,
            lyrics,
        )

        return {
            "primary_theme": primary_theme,
            "emotional_tone": emotional_tone,
            "visual_metaphors": visual_metaphors,
            "narrative_elements": narrative_elements,
        }

    def _extract_visual_metaphors(self, lyrics: str) -> str:
        """Extract visual metaphors from lyrics"""
        metaphors = []

        # Common visual metaphor patterns
        patterns = {
            "light": r"\b(light|glow|shine|bright|moon|sun|star|fire|flame)\b",
            "dark": r"\b(dark|shadow|night|black|void|empty|hollow)\b",
            "nature": r"\b(tree|leaf|wind|rain|storm|earth|sky|valley|mountain)\b",
            "urban": r"\b(city|street|alley|wall|concrete|neon|graffiti|trash)\b",
            "emotion": r"\b(heart|soul|pain|love|hate|fear|hope|dream|memory)\b",
        }

        for category, pattern in patterns.items():
            matches = re.findall(pattern, lyrics.lower())
            if matches:
                metaphors.append(f"{category}: {', '.join(set(matches))}")

        return "; ".join(metaphors)

    def _generate_narrative_elements(:
        self,
        theme: str,
        emotion: str,
        lyrics: str,
    ) -> dict[str, str]:
        """Generate narrative elements based on theme and emotion"""
        narrative_templates = {
            "nature": {
                "core_narrative": "A cinematic journey through nature's healing power, where broken hearts find solace in ancient wisdom",
                "emotional_journey": "From heartbreak to nature's embrace to healing transformation",
                "setting_atmosphere": "Mystical forest with ethereal beauty",
                "target_emotion": "Wonder and healing",
                "core_message": "Nature heals the broken heart",
            },
            "urban": {
                "core_narrative": "A raw, unfiltered rebellion against conventional love, where authenticity triumphs over pretense",
                "emotional_journey": "From romantic disillusionment to urban rebellion to authentic self",
                "setting_atmosphere": "Gritty urban alleyway with punk energy",
                "target_emotion": "Defiance and authenticity",
                "core_message": "Love is overrated, embrace your true self",
            },
            "blues": {
                "core_narrative": "An intimate journey through the healing power of music, where sorrow transforms into hope",
                "emotional_journey": "From emotional pain to musical expression to healing through art",
                "setting_atmosphere": "Intimate moonlit setting with musical atmosphere",
                "target_emotion": "Soulful reflection",
                "core_message": "Music speaks the truth of the heart",
            },
            "storm": {
                "core_narrative": "A dramatic journey through inner chaos to personal transformation, where storms become sources of power",
                "emotional_journey": "From inner chaos to storm mastery to phoenix transformation",
                "setting_atmosphere": "Dramatic stormy landscape with elemental power",
                "target_emotion": "Power and transformation",
                "core_message": "Embrace the storm within",
            },
            "folk": {
                "core_narrative": "A contemplative journey through unknown lands and inner transformation, where every step reveals new mysteries",
                "emotional_journey": "From aimless wandering to purposeful journey to self-discovery",
                "setting_atmosphere": "Mystical countryside with ancient wisdom",
                "target_emotion": "Contemplation and discovery",
                "core_message": "The journey is the destination",
            },
        }

        return narrative_templates.get(theme, narrative_templates["folk"])

    def generate_image_prompts(self, analysis: dict[str, any]) -> list[dict[str, str]]:
        """Generate detailed image prompts for visual storytelling"""
        theme = analysis["primary_theme"]
        emotion = analysis["emotional_tone"]
        narrative = analysis["narrative_elements"]

        # Image prompt templates based on theme
        prompt_templates = {
            "nature": self._generate_nature_prompts,
            "urban": self._generate_urban_prompts,
            "blues": self._generate_blues_prompts,
            "storm": self._generate_storm_prompts,
            "folk": self._generate_folk_prompts,
        }

        generator = prompt_templates.get(theme, self._generate_folk_prompts)
        return generator(analysis)

    def _generate_nature_prompts(:
        self,
        analysis: dict[str, any],
    ) -> list[dict[str, str]]:
        """Generate nature-themed image prompts"""
        return [
            {
                "title": "Moonlit Valleys Calling",
                "prompt": "A vast valley unfolds like an ancient manuscript under silver moonlight. A glowing willow tree stands sentinel at the heart, its delicate leaves shimmering and trembling like notes in nature's melancholic symphony. Mist rolls across the ground like liquid poetry, while fireflies punctuate the darkness with golden exclamation marks of light.",
                "typography": "Elegant serif font carved into natural wood, glowing softly with moonlight",
                "text": "Willow Whispers",
                "lighting": "Ethereal silvers bleeding into midnight blues with golden firefly accents",
                "color_scheme": "Silver-blue with golden whispers",
                "mood": "Contemplative",
            },
            {
                "title": "Heartbreak Like a Whisper",
                "prompt": "A close-up of a single willow branch trembling in the frame. Dewdrops cling to leaves like tears refusing to fall, each droplet capturing and refracting moonlight into a thousand tiny mirrors. Behind this crystalline curtain, a shadow-figure stands motionless—a monument to longing.",
                "typography": "Distorted, dripping paint effect with glitch elements",
                "text": "HEARTBREAK GROWS IN SILENCE",
                "lighting": "Cool blues cascading into grays—the color of 3 AM thoughts",
                "color_scheme": "Cool blues dissolving to gray",
                "mood": "Melancholic",
            },
            {
                "title": "Dancing with the Trees",
                "prompt": "The perspective weaves between willow branches like consciousness threading through dreams. Glowing orbs—memories made manifest—spiral upward, each one a captured moment refusing to be forgotten. The willow sways rhythmically, its leaves catching golden light like whispered secrets, forgotten promises, and tomorrow's possibilities.",
                "typography": "Organic, growing from bark with pulsing life energy",
                "text": "Hope and Memories, Dancing with the Trees",
                "lighting": "Warm golden memories clashing beautifully with cool night shadows",
                "color_scheme": "Golden warmth wrestling cool shadows",
                "mood": "Bittersweet",
            },
            {
                "title": "Hope That Never Dies",
                "prompt": "A lone figure stands beneath the willow, hand pressed against ancient bark in connection. Golden beams pierce through branches—dawn announcing itself with gentle violence. Fallen leaves suddenly rise, defying gravity, glowing as they ascend toward light that promises but doesn't guarantee.",
                "typography": "Light trails and ethereal, ascending letters",
                "text": "HOPE NEVER DIES",
                "lighting": "Silver moonlight evolving to golden sunrise",
                "color_scheme": "Silver moonlight evolving to sunrise",
                "mood": "Transformative",
            },
        ]

    def _generate_urban_prompts(self, analysis: dict[str, any]) -> list[dict[str, str]]:
        """Generate urban-themed image prompts"""
        return [
            {
                "title": "The Punk Raccoon Manifesto",
                "prompt": "A defiant raccoon in full punk attire—leather jacket studded with shattered hearts, spike collar catching streetlight like broken glass, smudged eyeliner showing vulnerability disguised as aggression. In one paw: a spray can hissing revolution. In the other: a wilted rose, beauty in decay.",
                "typography": "Neon graffiti in electric colors with dripping, rebellious energy",
                "text": "LOVE IS RUBBISH",
                "lighting": "Moody blacks and grays with neon explosions and golden streetlight flickers",
                "color_scheme": "Moody blacks with neon explosions",
                "mood": "Defiant",
            },
            {
                "title": "Trash Pandas Don't Do Romance",
                "prompt": "A gritty urban alleyway where love goes to die and be reborn as rebellion. Overflowing trash bins spill chocolate boxes and wilted roses. Cracked concrete foundation unable to hold the weight of broken promises. A raccoon stands defiant, spray-painting across the brick wall.",
                "typography": "Bold, rebellious typography with urban edge",
                "text": "TRASH PANDAS DON'T DO ROMANCE",
                "lighting": "Flickering streetlight with neon reflections",
                "color_scheme": "Moody blacks with neon pink, blood red, electric blue",
                "mood": "Rebellious",
            },
            {
                "title": "Anti-Valentine Forever",
                "prompt": "A close-up of a raccoon's gloved paw clutching a graffiti can, spraying across a wall covered in shattered heart stickers and broken promises. The scene is lit by harsh streetlight, creating dramatic shadows. Torn love letters litter the ground.",
                "typography": "Dripping, emotional typography with urban grit",
                "text": "Anti-Valentine FOREVER",
                "lighting": "Harsh streetlight with dramatic shadows",
                "color_scheme": "High contrast blacks with electric accents",
                "mood": "Raw",
            },
            {
                "title": "Love is a Dumpster Fire",
                "prompt": "A wide shot of an urban alleyway at night, with a raccoon standing triumphantly beside a burning dumpster. The flames illuminate graffiti that reads across the scene. Neon signs flicker in the background.",
                "typography": "Bold, fiery typography with urban energy",
                "text": "Love is a Dumpster Fire",
                "lighting": "Flaming dumpster with neon background",
                "color_scheme": "High contrast with fire and neon",
                "mood": "Intense",
            },
        ]

    def _generate_blues_prompts(self, analysis: dict[str, any]) -> list[dict[str, str]]:
        """Generate blues-themed image prompts"""
        return [
            {
                "title": "Midnight Serenade",
                "prompt": "A lone musician sits on a moonlit porch, guitar in hand, silhouetted against the night sky. The moon casts silver light across the scene, and fireflies dance in the background. The musician's head is bowed in concentration, lost in the music.",
                "typography": "Musical script with flowing, rhythmic lines",
                "text": "THE BLUES SPEAK TRUTH",
                "lighting": "Moonlight with soft, romantic glow",
                "color_scheme": "Deep blues with silver moonlight",
                "mood": "Soulful",
            },
            {
                "title": "Heartbreak Hotel",
                "prompt": "A dimly lit room where shadows dance on the walls. A figure sits alone at a table, head in hands, surrounded by empty bottles and scattered sheet music. The only light comes from a single candle, casting flickering shadows.",
                "typography": "Distressed, emotional handwriting",
                "text": "EVERY NOTE TELLS A LIE",
                "lighting": "Candlelight with dramatic shadows",
                "color_scheme": "Moody browns with golden candlelight",
                "mood": "Melancholic",
            },
            {
                "title": "The Healing Power",
                "prompt": "The same musician now stands in a moonlit field, guitar raised to the sky as if calling to the heavens. The music seems to flow from their soul, and the very air around them shimmers with the power of the blues.",
                "typography": "Dynamic, flowing energy waves",
                "text": "MUSIC HEALS THE SOUL",
                "lighting": "Ethereal moonlight with energy waves",
                "color_scheme": "Deep blues with ethereal silver",
                "mood": "Transcendent",
            },
            {
                "title": "Dawn's Redemption",
                "prompt": "The musician walks away from the field as dawn breaks, guitar slung over their shoulder. The night's sorrow has been transformed into morning's hope, and the blues have done their healing work.",
                "typography": "Warm, ascending light trails",
                "text": "THE BLUES NEVER LIE",
                "lighting": "Golden sunrise with warm light",
                "color_scheme": "Warm golds with ethereal glow",
                "mood": "Redemptive",
            },
        ]

    def _generate_storm_prompts(self, analysis: dict[str, any]) -> list[dict[str, str]]:
        """Generate storm-themed image prompts"""
        return [
            {
                "title": "The Gathering Storm",
                "prompt": "A figure stands on a cliff edge as dark storm clouds gather overhead. Lightning crackles in the distance, and the wind whips their hair and clothes. The sea below churns with white-capped waves.",
                "typography": "Electric, jagged lightning typography",
                "text": "THE STORM IS COMING",
                "lighting": "Dramatic storm lighting with lightning",
                "color_scheme": "Dark grays with electric blue lightning",
                "mood": "Intense",
            },
            {
                "title": "The Eye of the Storm",
                "prompt": "The figure stands in the center of a massive tornado, surrounded by swirling debris and howling winds. Yet they remain calm and centered, as if the storm itself is part of them.",
                "typography": "Dynamic, spiraling wind typography",
                "text": "I AM THE STORM",
                "lighting": "Tornado lighting with dramatic shadows",
                "color_scheme": "Dark grays with electric energy",
                "mood": "Chaotic",
            },
            {
                "title": "The Calm After",
                "prompt": "The storm passes, and the figure stands in the aftermath—damaged but not broken. The sky begins to clear, and rays of sunlight break through the clouds.",
                "typography": "Warm, ascending light trails",
                "text": "AFTER THE STORM COMES PEACE",
                "lighting": "Golden sunlight breaking through clouds",
                "color_scheme": "Warm golds with ethereal light",
                "mood": "Redemptive",
            },
            {
                "title": "The Phoenix Rising",
                "prompt": "The figure transforms into a phoenix, rising from the ashes of the storm. Wings spread wide, they soar into the clear sky above.",
                "typography": "Fiery, ascending flame typography",
                "text": "FROM DESTRUCTION COMES REBIRTH",
                "lighting": "Golden firelight with ethereal glow",
                "color_scheme": "Warm golds with fiery reds",
                "mood": "Transcendent",
            },
        ]

    def _generate_folk_prompts(self, analysis: dict[str, any]) -> list[dict[str, str]]:
        """Generate folk-themed image prompts"""
        return [
            {
                "title": "The Lonely Road",
                "prompt": "A lone figure walks down a desolate country road at twilight, carrying a worn leather satchel and a guitar case. The road stretches endlessly into the distance, lined with bare trees that seem to whisper secrets.",
                "typography": "Weathered, rustic typography carved into wood",
                "text": "THE ROAD GOES ON FOREVER",
                "lighting": "Twilight with long shadows and mist",
                "color_scheme": "Muted earth tones with golden hour light",
                "mood": "Melancholic",
            },
            {
                "title": "Midnight Crossroads",
                "prompt": "The traveler reaches a crossroads at midnight, where four paths meet under a gnarled oak tree. The moon hangs low in the sky, casting silver light on weathered signposts. Each path leads to a different destiny.",
                "typography": "Ancient runes with mystical glow",
                "text": "CHOOSE YOUR PATH",
                "lighting": "Moonlight with mystical silver glow",
                "color_scheme": "Deep blues with silver moonlight",
                "mood": "Mysterious",
            },
            {
                "title": "The Weary Wanderer",
                "prompt": "A close-up of the traveler's weathered hands holding a map that's been folded and refolded countless times. The map shows paths that have been crossed out and new routes drawn in. A campfire burns nearby.",
                "typography": "Handwritten script with personal touch",
                "text": "EVERY MILE TELLS A STORY",
                "lighting": "Campfire light with warm, intimate glow",
                "color_scheme": "Warm earth tones with firelight",
                "mood": "Intimate",
            },
            {
                "title": "Dawn's New Beginning",
                "prompt": "The traveler reaches a hilltop at dawn, looking out over a vast landscape that stretches to the horizon. The sun rises behind them, casting their shadow long across the valley below.",
                "typography": "Ethereal, ascending light trails",
                "text": "THE JOURNEY NEVER ENDS",
                "lighting": "Golden sunrise with ethereal light",
                "color_scheme": "Warm golds with ethereal glow",
                "mood": "Hopeful",
            },
        ]

    def generate_youtube_title(self, song_title: str, theme: str, emotion: str) -> str:
        """Generate SEO-optimized YouTube title"""
        emoji_map = {
            "nature": "🌙",
            "urban": "🔥",
            "blues": "🎵",
            "storm": "⚡",
            "folk": "🌙",
        }

        style_map = {
            "nature": "Ethereal Folk Journey",
            "urban": "Punk Rebellion",
            "blues": "Soulful Blues",
            "storm": "Epic Transformation",
            "folk": "Mystical Journey",
        }

        emoji = emoji_map.get(theme, "🎵")
        style = style_map.get(theme, "Musical Journey")

        return f"{emoji} {song_title.upper()}: {style} | Indie Music Visual Story"

    def generate_seo_keywords(self, theme: str, emotion: str, visual_style: str) -> str:
        """Generate SEO keywords for discoverability"""
        keyword_sets = {
            "nature": [
                "ethereal folk",
                "moonlit healing",
                "indie music",
                "nature sanctuary",
                "heartbreak healing",
                "willow tree",
                "mystical journey",
            ],
            "urban": [
                "punk raccoon",
                "anti-valentine",
                "urban rebellion",
                "graffiti music",
                "trash pandas",
                "neon punk",
                "love cynicism",
            ],
            "blues": [
                "moonlit blues",
                "soulful guitar",
                "blues music",
                "midnight serenade",
                "emotional healing",
                "musical expression",
            ],
            "storm": [
                "stormchild",
                "inner transformation",
                "powerful music",
                "epic storm",
                "phoenix rising",
                "personal growth",
            ],
            "folk": [
                "dark folk",
                "mystical journey",
                "midnight crossroads",
                "indie music",
                "wandering solitude",
                "self-discovery",
            ],
        }

        keywords = keyword_sets.get(
            theme,
            ["indie music", "emotional journey", "visual storytelling"],
        )
        return ", ".join(keywords)

    def generate_digital_dive_instructions(:
        self,
        theme: str,
        aspect_ratio: str = "9:16",
    ) -> str:
        """Generate DALL-E 3 instructions for image generation"""
        instructions = {
            "nature": f"Generate 4 cinematic images using DALL-E 3 with {aspect_ratio} aspect ratio, focusing on ethereal moonlight, mystical willow imagery, and emotional healing through nature",
            "urban": f"Generate 4 dynamic images using DALL-E 3 with {aspect_ratio} aspect ratio, featuring punk raccoon character, neon graffiti, and urban rebellion aesthetics",
            "blues": f"Generate 4 intimate images using DALL-E 3 with {aspect_ratio} aspect ratio, featuring moonlit scenes, musical instruments, and emotional depth",
            "storm": f"Generate 4 epic images using DALL-E 3 with {aspect_ratio} aspect ratio, featuring dramatic storms, lightning, and transformative imagery",
            "folk": f"Generate 4 atmospheric images using DALL-E 3 with {aspect_ratio} aspect ratio, focusing on mystical landscapes, weathered textures, and contemplative solitude",
        }

        return instructions.get(
            theme,
            f"Generate 4 cinematic images using DALL-E 3 with {aspect_ratio} aspect ratio",
        )

    def create_comprehensive_analysis(self, song_data: dict[str, str]) -> SongAnalysis:
        """Create comprehensive song analysis using all methods"""
        # Analyze lyrics
        analysis = self.analyze_lyrics(song_data.get("lyrics", ""))

        # Generate image prompts
        image_prompts = self.generate_image_prompts(analysis)

        # Create comprehensive analysis
        return SongAnalysis(
            song_title=song_data.get("title", "Unknown Song"),
            genre_fusion=f"{analysis['primary_theme'].title()} {analysis['emotional_tone'].title()}",
            primary_theme=analysis["primary_theme"],
            secondary_theme=analysis["narrative_elements"].get(
                "secondary_theme",
                "Emotional Journey",
            ),
            emotional_tone=analysis["emotional_tone"],
            visual_style=self.visual_styles.get(
                analysis["primary_theme"],
                "Moody Atmospheric",
            ),
            image_series_title=f"{analysis['primary_theme'].title()} Series",
            core_narrative=analysis["narrative_elements"]["core_narrative"],
            visual_metaphors=analysis["visual_metaphors"],
            emotional_journey=analysis["narrative_elements"]["emotional_journey"],
            character_archetype=self.character_archetypes.get(
                analysis["primary_theme"],
                "The Wandering Seeker",
            ),
            setting_atmosphere=analysis["narrative_elements"]["setting_atmosphere"],
            target_emotion=analysis["narrative_elements"]["target_emotion"],
            core_message=analysis["narrative_elements"]["core_message"],
            youtube_title=self.generate_youtube_title(
                song_data.get("title", ""),
                analysis["primary_theme"],
                analysis["emotional_tone"],
            ),
            seo_keywords=self.generate_seo_keywords(
                analysis["primary_theme"],
                analysis["emotional_tone"],
                self.visual_styles.get(analysis["primary_theme"]),
            ),
            digital_dive_instructions=self.generate_digital_dive_instructions(
                analysis["primary_theme"],
            ),
        )


def main():
    """Main function to demonstrate usage"""
    generator = SongAnalysisGenerator()

    # Example song data
    sample_song = {
        "title": "Willow Whispers",
        "lyrics": "In moonlit alleys we used to sing, Now I roam these streets alone, Beneath the stars my heart it stings, Darkened nights I've always known...",
    }

    # Generate analysis
    analysis = generator.create_comprehensive_analysis(sample_song)

    print(f"Song: {analysis.song_title}")
    print(f"Genre: {analysis.genre_fusion}")
    print(f"Primary Theme: {analysis.primary_theme}")
    print(f"Emotional Tone: {analysis.emotional_tone}")
    print(f"Core Narrative: {analysis.core_narrative}")
    print(f"YouTube Title: {analysis.youtube_title}")
    print(f"SEO Keywords: {analysis.seo_keywords}")


if __name__ == "__main__":
    main()
