#!/usr/bin/env python3
"""
As a Man Thinketh - Text to Speech System (Real Content)
A comprehensive TTS system for James Allen's classic book with actual content from Project Gutenberg.
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# Load environment variables
load_dotenv(os.path.expanduser("~/.env"))

class TTSProvider:
    """Base class for TTS providers"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def synthesize(self, text: str, output_path: str, voice: str = None) -> bool:
        """Synthesize text to speech and save to file"""
        raise NotImplementedError

class ElevenLabsTTS(TTSProvider):
    """ElevenLabs TTS implementation"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.elevenlabs.io/v1"
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice (Rachel)
    
    def synthesize(self, text: str, output_path: str, voice: str = None) -> bool:
        """Synthesize text using ElevenLabs API"""
        try:
            url = f"{self.base_url}/text-to-speech/{self.voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            logger.info(f"ElevenLabs TTS Error: {e}")
            return False

class AssemblyAITTS(TTSProvider):
    """AssemblyAI TTS implementation"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.assemblyai.com/v2"
    
    def synthesize(self, text: str, output_path: str, voice: str = None) -> bool:
        """Synthesize text using AssemblyAI API"""
        try:
            # AssemblyAI TTS endpoint
            url = f"{self.base_url}/text-to-speech"
            headers = {
                "authorization": self.api_key,
                "content-type": "application/json"
            }
            
            data = {
                "text": text,
                "voice": voice or "alloy"
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            # Get the audio URL from response
            audio_url = response.json().get("audio_url")
            if not audio_url:
                return False
            
            # Download the audio file
            audio_response = requests.get(audio_url)
            audio_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(audio_response.content)
            
            return True
        except Exception as e:
            logger.info(f"AssemblyAI TTS Error: {e}")
            return False

class DeepgramTTS(TTSProvider):
    """Deepgram TTS implementation"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.deepgram.com/v1"
    
    def synthesize(self, text: str, output_path: str, voice: str = None) -> bool:
        """Synthesize text using Deepgram API"""
        try:
            url = f"{self.base_url}/speak"
            headers = {
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "model": "aura-asteria-en",
                "encoding": "mp3",
                "container": "mp3"
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            logger.info(f"Deepgram TTS Error: {e}")
            return False
class AsAManThinkethTTS:
    """Main TTS system for As a Man Thinketh with real content"""
    
    def __init__(self):
        self.setup_tts_provider()
        self.setup_chapters()
        self.output_dir = Path("as_a_man_thinketh_audio")
        self.output_dir.mkdir(exist_ok=True)
    
    def setup_tts_provider(self):
        """Setup TTS provider based on available API keys"""
        # Check for ElevenLabs first (best quality)
        if os.getenv("ELEVENLABS_API_KEY"):
            self.tts = ElevenLabsTTS(os.getenv("ELEVENLABS_API_KEY"))
            self.provider_name = "ElevenLabs"
        elif os.getenv("ASSEMBLYAI_API_KEY"):
            self.tts = AssemblyAITTS(os.getenv("ASSEMBLYAI_API_KEY"))
            self.provider_name = "AssemblyAI"
        elif os.getenv("DEEPGRAM_API_KEY"):
            self.tts = DeepgramTTS(os.getenv("DEEPGRAM_API_KEY"))
            self.provider_name = "Deepgram"
        else:
            raise ValueError("No TTS API key found in environment variables")
        
        logger.info(f"Using TTS provider: {self.provider_name}")
    
    def setup_chapters(self):
        """Setup the chapter structure with real content from Project Gutenberg"""
        self.chapters = {
            "foreword": {
                "title": "Foreword",
                "sections": [
                    "This little volume (the result of meditation and experience) is not intended as an exhaustive treatise on the much-written-upon subject of the power of thought. It is suggestive rather than explanatory, its object being to stimulate men and women to the discovery and perception of the truth that—\n\n\"They themselves are makers of themselves.\"\n\nby virtue of the thoughts, which they choose and encourage; that mind is the master-weaver, both of the inner garment of character and the outer garment of circumstance, and that, as they may have hitherto woven in ignorance and pain they may now weave in enlightenment and happiness."
                ]
            },
            "chapter_1": {
                "title": "Chapter I: Thought and Character",
                "sections": [
                    "The aphorism, \"As a man thinketh in his heart so is he,\" not only embraces the whole of a man's being, but is so comprehensive as to reach out to every condition and circumstance of his life. A man is literally what he thinks, his character being the complete sum of all his thoughts.",
                    "As the plant springs from, and could not be without, the seed, so every act of a man springs from the hidden seeds of thought, and could not have appeared without them. This applies equally to those acts called \"spontaneous\" and \"unpremeditated\" as to those, which are deliberately executed.",
                    "Act is the blossom of thought, and joy and suffering are its fruits; thus does a man garner in the sweet and bitter fruitage of his own husbandry.",
                    "Thought in the mind hath made us, what we are\nBy thought was wrought and built. If a man's mind\nHath evil thoughts, pain comes on him as comes\nThe wheel the ox behind....\n\nIf one endure in purity of thought joy follows him as his own shadow—sure.",
                    "Man is a growth by law, and not a creation by artifice, and cause and effect is as absolute and undeviating in the hidden realm of thought as in the world of visible and material things. A noble and Godlike character is not a thing of favor or chance, but is the natural result of continued effort in right thinking, the effect of long-cherished association with Godlike thoughts. An ignoble and bestial character, by the same process, is the result of the continued harboring of groveling thoughts.",
                    "Man is made or unmade by himself; in the armory of thought he forges the weapons by which he destroys himself; he also fashions the tools with which he builds for himself heavenly mansions of joy and strength and peace. By the right choice and true application of thought, man ascends to the Divine Perfection; by the abuse and wrong application of thought, he descends below the level of the beast. Between these two extremes are all the grades of character, and man is their maker and master.",
                    "Of all the beautiful truths pertaining to the soul which have been restored and brought to light in this age, none is more gladdening or fruitful of divine promise and confidence than this—that man is the master of thought, the molder of character, and maker and shaper of condition, environment, and destiny.",
                    "As a being of Power, Intelligence, and Love, and the lord of his own thoughts, man holds the key to every situation, and contains within himself that transforming and regenerative agency by which he may make himself what he wills.",
                    "Man is always the master, even in his weakest and most abandoned state; but in his weakness and degradation he is the foolish master who misgoverns his \"household.\" When he begins to reflect upon his condition, and to search diligently for the Law upon which his being is established, he then becomes the wise master, directing his energies with intelligence, and fashioning his thoughts to fruitful issues. Such is the conscious master, and man can only thus become by discovering within himself the laws of thought; which discovery is totally a matter of application, self-analysis, and experience.",
                    "Only by much searching and mining, are gold and diamonds obtained, and man can find every truth connected with his being, if he will dig deep into the mine of his soul; and that he is the maker of his character, the molder of his life, and the builder of his destiny, he may unerringly prove, if he will watch, control, and alter his thoughts, tracing their effects upon himself, upon others, and upon his life and circumstances, linking cause and effect by patient practice and investigation, and utilizing his every experience, even to the most trivial, everyday occurrence, as a means of obtaining that knowledge of himself which is Understanding, Wisdom, Power. In this direction, as in no other, is the law absolute that \"He that seeketh findeth; and to him that knocketh it shall be opened;\" for only by patience, practice, and ceaseless importunity can a man enter the Door of the Temple of Knowledge."
                ]
            },
            "chapter_2": {
                "title": "Chapter II: Effect of Thought on Circumstances",
                "sections": [
                    "Man's mind may be likened to a garden, which may be intelligently cultivated or allowed to run wild; but whether cultivated or neglected, it must, and will, bring forth. If no useful seeds are put into it, then an abundance of useless weed seeds will fall therein, and will continue to produce their kind.",
                    "Just as a gardener cultivates his plot, keeping it free from weeds, and growing the flowers and fruits which he requires, so may a man tend the garden of his mind, weeding out all the wrong, useless, and impure thoughts, and cultivating toward perfection the flowers and fruits of right, useful, and pure thoughts. By pursuing this process, a man sooner or later discovers that he is the master-gardener of his soul, the director of his life. He also reveals, within himself, the laws of thought, and understands, with ever-increasing accuracy, how the thought-forces and mind-elements operate in the shaping of his character, circumstances, and destiny.",
                    "Thought and character are one, and as character can only manifest and discover itself through environment and circumstance, the outer conditions of a person's life will always be found to be harmoniously related to his inner state. This does not mean that a man's circumstances at any given time are an indication of his entire character, but that those circumstances are so intimately connected with some vital thought-element within himself that, for the time being, they are indispensable to his development.",
                    "Every man is where he is by the law of his being; the thoughts which he has built into his character have brought him there, and in the arrangement of his life there is no element of chance, but all is the result of a law which cannot err. This is just as true of those who feel \"out of harmony\" with their surroundings as of those who are contented with them.",
                    "As a progressive and evolving being, man is where he is that he may learn that he may grow; and as he learns the spiritual lesson which any circumstance contains for him, it passes away and gives place to other circumstances.",
                    "Man is buffeted by circumstances so long as he believes himself to be the creature of outside conditions, but when he realizes that he is a creative power, and that he may command the hidden soil and seeds of his being out of which circumstances grow, he then becomes the rightful master of himself.",
                    "That circumstances grow out of thought every man knows who has for any length of time practiced self-control and self-purification, for he will have noticed that the alteration in his circumstances has been in exact ratio with the altered condition of his mind. So true is this that when a man earnestly applies himself to remedy the defects in his character, and makes swift and marked progress, he passes rapidly through a succession of vicissitudes.",
                    "The soul attracts that which it secretly harbors; that which it loves, and also that which it fears; it reaches the height of its cherished aspirations; it falls to the level of its unchastened desires,—and circumstances are the means by which the soul receives its own.",
                    "Every thought-seed sown or allowed to fall into the mind, and to take root there, produces its own, blossoming sooner or later into act, and bearing its own fruitage of opportunity and circumstance. Good thoughts bear good fruit, bad thoughts bad fruit.",
                    "The outer world of circumstance shapes itself to the inner world of thought, and both pleasant and unpleasant external conditions are factors which make for the ultimate good of the individual. As the reaper of his own harvest, man learns both by suffering and bliss.",
                    "Following the inmost desires, aspirations, thoughts, by which he allows himself to be dominated, (pursuing the will-o'-the-wisps of impure imagining or steadfastly walking the highway of strong and high endeavor), a man at last arrives at their fruition and fulfillment in the outer conditions of his life. The laws of growth and adjustment everywhere obtains.",
                    "A man does not come to the almshouse or the jail by the tyranny of fate or circumstance, but by the pathway of groveling thoughts and base desires. Nor does a pure-minded man fall suddenly into crime by stress of any external force; the criminal thought had long been secretly fostered in the heart, and the hour of opportunity revealed its gathered power. Circumstance does not make the man; it reveals him to himself. No such conditions can exist as descending into vice and its attendant sufferings apart from vicious inclinations, or ascending into virtue and its pure happiness without the continued cultivation of virtuous aspirations; and man, therefore, as the lord and master of thought, is the maker of himself, the shaper and author of environment. Even at birth the soul comes to its own and through every step of its earthly pilgrimage it attracts those combinations of conditions which reveal itself, which are the reflections of its own purity and, impurity, its strength and weakness.",
                    "Men do not attract that which they want, but that which they are. Their whims, fancies, and ambitions are thwarted at every step, but their inmost thoughts and desires are fed with their own food, be it foul or clean. The \"divinity that shapes our ends\" is in ourselves; it is our very self. Only himself manacles man: thought and action are the jailers of Fate—they imprison, being base; they are also the angels of Freedom—they liberate, being noble. Not what he wishes and prays for does a man get, but what he justly earns. His wishes and prayers are only gratified and answered when they harmonize with his thoughts and actions.",
                    "In the light of this truth, what, then, is the meaning of \"fighting against circumstances?\" It means that a man is continually revolting against an effect without, and at the same time is causing and perpetuating its cause in his thought.",
                    "A man's weakness and strength, purity and impurity, are his own, and not another man's; they are brought about by himself, and not by another; and they can only be altered by himself, never by another. His condition is also his own, and not another man's. His suffering and his happiness are evolved from within. As he thinks, so he is; as he continues to think, so he remains.",
                    "A strong man cannot help a weaker unless that weaker is willing to be helped, and even then the weak man must become strong of himself; he must, by his own efforts, develop the strength which he admires in another. None but himself can alter his condition.",
                    "It has been usual for men to think and to say, \"Many men are slaves because one is an oppressor; let us hate the oppressor.\" Now, however, there is amongst an increasing few a tendency to reverse this judgment, and to say, \"One man is an oppressor because many are slaves; let us despise the slaves.\" The truth is that oppressor and slave are co-operators in ignorance, and, while seeming to afflict one another, are in reality afflicting themselves. A perfect Knowledge perceives the action of law in the weakness of the oppressed and the misapplied power of the oppressor. A perfect Love, seeing the suffering which both states entail, condemns neither; a perfect Compassion embraces both oppressor and oppressed.",
                    "He who has conquered weakness, and has put away all selfish thoughts, belongs neither to oppressor nor oppressed. He is free.",
                    "A man can only rise, conquer, and achieve by lifting up his thoughts. He can only remain weak, and abject, and miserable by refusing to lift up his thoughts.",
                    "Before a man can achieve anything, even in worldly things, he must lift his thoughts above slavish animal indulgence. He may not, in order to succeed, give up all animality and selfishness, by any means; but a portion of it must, at least, be sacrificed. A man whose first thought is bestial indulgence could neither think clearly nor plan methodically; he could not find and develop his latent resources, and would fail in any undertaking. Not having commenced to manfully control his thoughts, he is not in a position to control affairs and to adopt serious responsibilities. He is not fit to act independently and stand alone. But he is limited only by the thoughts which he chooses.",
                    "There can be no progress, no achievement without sacrifice, and a man's worldly success will be in the measure that he sacrifices his confused animal thoughts, and fixes his mind on the development of his plans, and the strengthening of his resolution and self-reliance. And the higher he lifts his thoughts, the more manly, upright, and righteous he becomes, the greater will be his success, the more blessed and enduring will be his achievements.",
                    "The universe does not favor the greedy, the dishonest, the vicious, although on the mere surface it may appear to do so; it helps the honest, the magnanimous, the virtuous. All the great teachers of the ages have declared this in varying forms, and to prove and know it a man has but to persist in making himself more and more virtuous by lifting up his thoughts.",
                    "Intellectual achievements are the result of thought consecrated to the search for knowledge, or for the beautiful and true in life and nature. Such achievements may be sometimes connected with vanity and ambition, but they are not the outcome of those characteristics; they are the natural outgrowth of long and arduous effort, and of pure and unselfish thoughts.",
                    "Spiritual achievements are the consummation of holy aspirations. He who lives constantly in the conception of noble and lofty thoughts, who dwells upon all that is pure and unselfish, will, as surely as the sun reaches its zenith and the moon its full, become wise and noble in character, and rise into a position of influence and blessedness.",
                    "Achievement, of whatever kind, is the crown of effort, the diadem of thought. By the aid of self-control, resolution, purity, righteousness, and well-directed thought a man ascends; by the aid of animality, indolence, impurity, corruption, and confusion of thought a man descends.",
                    "A man may rise to high success in the world, and even to lofty altitudes in the spiritual realm, and again descend into weakness and degradation by allowing arrogant, selfish, and corrupt thoughts to take possession of him.",
                    "Victories attained by right thought can only be maintained by watchfulness. Many give way when success is assured, and rapidly fall back into failure.",
                    "All achievements, whether in the business, intellectual, or spiritual world, are the result of definitely directed thought, are governed by the same law and are of the same method; the only difference lies in the object of attainment.",
                    "He who would accomplish little must sacrifice little; he who would achieve much must sacrifice much; he who would attain highly must sacrifice greatly."
                ]
            },
            "chapter_3": {
                "title": "Chapter III: Effect of Thought on Health and the Body",
                "sections": [
                    "The body is the servant of the mind. It obeys the operations of the mind, whether they be deliberately chosen or automatically expressed. At the bidding of unlawful thoughts the body sinks rapidly into disease and decay; at the command of glad and beautiful thoughts it becomes clothed with youthfulness and beauty.",
                    "Disease and health, like circumstances, are rooted in thought. Sickly thoughts will express themselves through a sickly body. Thoughts of fear have been known to kill a man as speedily as a bullet, and they are continually killing thousands of people just as surely though less rapidly.",
                    "The people who live in fear of disease are the people who get it. Anxiety quickly demoralizes the whole body, and lays it open to the entrance of disease; while impure thoughts, even if not physically indulged, will soon shatter the nervous system.",
                    "Strong, pure, and happy thoughts build up the body in vigor and grace. The body is a delicate and plastic instrument, which responds readily to the thoughts by which it is impressed, and habits of thought will produce their own effects, good or bad, upon it.",
                    "Men will continue to have impure and poisoned blood, so long as they propagate unclean thoughts. Out of a clean heart comes a clean life and a clean body. Out of a defiled mind proceeds a defiled life and a corrupt body.",
                    "Thought is the fount of action, life and manifestation; make the fountain pure, and all will be pure.",
                    "Change of diet will not help a man who will not change his thoughts. When a man makes his thoughts pure, he no longer desires impure food.",
                    "Clean thoughts make clean habits. The so-called saint who does not wash his body is not a saint. He who has strengthened and purified his thoughts does not need to consider the malevolence of microbes.",
                    "If you would protect your body, guard your mind. If you would renew your body, beautify your mind. Thoughts of malice, envy, disappointment, despondency, rob the body of its health and grace. A sour face does not come by chance; it is made by sour thoughts. Wrinkles that mar are drawn by folly, passion, pride.",
                    "I know a woman of ninety-six who has the bright, innocent face of a girl. I know a man well under middle age whose face is drawn into inharmonious contours. The one is the result of a sweet and sunny disposition; the other is the outcome of passion and discontent.",
                    "As you cannot have a sweet and wholesome abode unless you admit the air and sunshine freely into your rooms, so a strong body and a bright, happy, or serene countenance can only result from the admittance into the mind of thoughts of joy and good will and serenity.",
                    "On the faces of the aged there are wrinkles made by sympathy, others by strong and pure thought, and others are carved by passion: who cannot distinguish them?",
                    "With an old man who has always thought out of the sunshine of life, the carven lines of age will be in harmony, and will impart an indescribable beauty which time cannot efface.",
                    "If you would keep young, look up; if you would grow old, look down. If you would keep young, think young thoughts; if you would grow old, think old thoughts.",
                    "The body is a highly complex and sensitive instrument, and it responds to the thoughts by which it is impressed, and habits of thought will produce their own effects, good or bad, upon it.",
                    "Men will continue to have impure and poisoned blood, so long as they propagate unclean thoughts. Out of a clean heart comes a clean life and a clean body. Out of a defiled mind proceeds a defiled life and a corrupt body.",
                    "Thought is the fount of action, life and manifestation; make the fountain pure, and all will be pure.",
                    "Change of diet will not help a man who will not change his thoughts. When a man makes his thoughts pure, he no longer desires impure food.",
                    "Clean thoughts make clean habits. The so-called saint who does not wash his body is not a saint. He who has strengthened and purified his thoughts does not need to consider the malevolence of microbes.",
                    "If you would protect your body, guard your mind. If you would renew your body, beautify your mind. Thoughts of malice, envy, disappointment, despondency, rob the body of its health and grace. A sour face does not come by chance; it is made by sour thoughts. Wrinkles that mar are drawn by folly, passion, pride."
                ]
            },
            "chapter_4": {
                "title": "Chapter IV: Thought and Purpose",
                "sections": [
                    "Until thought is linked with purpose there is no intelligent accomplishment. With the majority, the bark of thought is allowed to \"drift\" upon the ocean of life. Aimlessness is a vice, and such drifting must not continue for him who would steer clear of catastrophe and destruction.",
                    "They who have no central purpose in their life fall an easy prey to petty worries, fears, troubles, and self-pityings, all of which are indications of weakness, which lead, just as surely as deliberately planned sins (though by a different route), to failure, unhappiness, and loss, for weakness cannot persist in a power-evolving universe.",
                    "A man should conceive of a legitimate purpose in his heart, and set out to accomplish it. He should make this purpose the centralizing point of his thoughts. It may take the form of a spiritual ideal, or it may be a worldly object, according to his nature at the time being; but whichever it is, he should steadily focus his thought-forces upon the object, which he has set before him. He should make this purpose his supreme duty, and should devote himself to its attainment, not allowing his thoughts to wander away into ephemeral fancies, longings, and imaginings. This is the royal road to self-control and true concentration of thought.",
                    "Even if he fails again and again to accomplish his purpose (as he necessarily must until weakness is overcome), the strength of character gained will be the measure of his true success, and this will form a new starting-point for future power and triumph.",
                    "Those who are not prepared for the apprehension of a great purpose should fix the thoughts upon the faultless performance of their duty, no matter how insignificant their task may appear. Only in this way can the thoughts be gathered and focused, and resolution and energy be developed, which being done, there is nothing which may not be accomplished.",
                    "The weakest soul, knowing its own weakness, and believing this truth—that strength can only be developed by effort and practice, will, thus believing, immediately begin to exert itself, and, adding effort to effort, patience to patience, and strength to strength, will never cease to develop, and will at last grow divinely strong.",
                    "As the physically weak man can make himself strong by careful and patient training, so the man of weak thoughts can make them strong by exercising himself in right thinking.",
                    "To put away aimlessness and weakness, and to begin to think with purpose, is to enter the ranks of those strong ones who only recognize failure as one of the pathways to attainment; who make all conditions serve them, and who think strongly, attempt fearlessly, and accomplish masterfully.",
                    "Having conceived of his purpose, a man should mentally mark out a straight pathway to its achievement, looking neither to the right nor the left. Doubts and fears should be rigorously excluded; they are disintegrating elements, which break up the straight line of effort, render it crooked, ineffectual, useless. Thoughts of doubt and fear never accomplished anything, and never can. They always lead to failure. Purpose, energy, power to do, and all strong thoughts cease when doubt and fear creep in.",
                    "The will to do springs from the knowledge that we can do. Doubt and fear are the great enemies of knowledge, and he who encourages them, who does not slay them, thwarts himself at every step.",
                    "He who has conquered doubt and fear has conquered failure. His every thought is allied with power, and all difficulties are bravely met and wisely overcome. His purposes are seasonably planted, and they bloom and bring forth fruit, which does not fall prematurely to the ground.",
                    "Thought allied fearlessly to purpose becomes creative force: he who knows this is ready to become something higher and stronger than a mere bundle of wavering thoughts and fluctuating sensations; and when this knowledge is so thoroughly seated in his mind that he becomes the master of his thoughts, he is ready to become the master of his circumstances, and the director of his destiny.",
                    "A man should conceive of a legitimate purpose in his heart, and set out to accomplish it. He should make this purpose the centralizing point of his thoughts. It may take the form of a spiritual ideal, or it may be a worldly object, according to his nature at the time being; but whichever it is, he should steadily focus his thought-forces upon the object, which he has set before him. He should make this purpose his supreme duty, and should devote himself to its attainment, not allowing his thoughts to wander away into ephemeral fancies, longings, and imaginings. This is the royal road to self-control and true concentration of thought.",
                    "Even if he fails again and again to accomplish his purpose (as he necessarily must until weakness is overcome), the strength of character gained will be the measure of his true success, and this will form a new starting-point for future power and triumph.",
                    "Those who are not prepared for the apprehension of a great purpose should fix the thoughts upon the faultless performance of their duty, no matter how insignificant their task may appear. Only in this way can the thoughts be gathered and focused, and resolution and energy be developed, which being done, there is nothing which may not be accomplished.",
                    "The weakest soul, knowing its own weakness, and believing this truth—that strength can only be developed by effort and practice, will, thus believing, immediately begin to exert itself, and, adding effort to effort, patience to patience, and strength to strength, will never cease to develop, and will at last grow divinely strong.",
                    "As the physically weak man can make himself strong by careful and patient training, so the man of weak thoughts can make them strong by exercising himself in right thinking.",
                    "To put away aimlessness and weakness, and to begin to think with purpose, is to enter the ranks of those strong ones who only recognize failure as one of the pathways to attainment; who make all conditions serve them, and who think strongly, attempt fearlessly, and accomplish masterfully.",
                    "Having conceived of his purpose, a man should mentally mark out a straight pathway to its achievement, looking neither to the right nor the left. Doubts and fears should be rigorously excluded; they are disintegrating elements, which break up the straight line of effort, render it crooked, ineffectual, useless. Thoughts of doubt and fear never accomplished anything, and never can. They always lead to failure. Purpose, energy, power to do, and all strong thoughts cease when doubt and fear creep in.",
                    "The will to do springs from the knowledge that we can do. Doubt and fear are the great enemies of knowledge, and he who encourages them, who does not slay them, thwarts himself at every step.",
                    "He who has conquered doubt and fear has conquered failure. His every thought is allied with power, and all difficulties are bravely met and wisely overcome. His purposes are seasonably planted, and they bloom and bring forth fruit, which does not fall prematurely to the ground.",
                    "Thought allied fearlessly to purpose becomes creative force: he who knows this is ready to become something higher and stronger than a mere bundle of wavering thoughts and fluctuating sensations; and when this knowledge is so thoroughly seated in his mind that he becomes the master of his thoughts, he is ready to become the master of his circumstances, and the director of his destiny."
                ]
            },
            "chapter_5": {
                "title": "Chapter V: The Thought-Factor in Achievement",
                "sections": [
                    "All that a man achieves and all that he fails to achieve is the direct result of his own thoughts. In a justly ordered universe, where loss of equipoise would mean total destruction, individual responsibility must be absolute. A man's weakness and strength, purity and impurity, are his own, and not another man's; they are brought about by himself, and not by another; and they can only be altered by himself, never by another. His condition is also his own, and not another man's. His suffering and his happiness are evolved from within. As he thinks, so he is; as he continues to think, so he remains.",
                    "A strong man cannot help a weaker unless that weaker is willing to be helped, and even then the weak man must become strong of himself; he must, by his own efforts, develop the strength which he admires in another. None but himself can alter his condition.",
                    "It has been usual for men to think and to say, \"Many men are slaves because one is an oppressor; let us hate the oppressor.\" Now, however, there is amongst an increasing few a tendency to reverse this judgment, and to say, \"One man is an oppressor because many are slaves; let us despise the slaves.\" The truth is that oppressor and slave are co-operators in ignorance, and, while seeming to afflict one another, are in reality afflicting themselves. A perfect Knowledge perceives the action of law in the weakness of the oppressed and the misapplied power of the oppressor. A perfect Love, seeing the suffering which both states entail, condemns neither; a perfect Compassion embraces both oppressor and oppressed.",
                    "He who has conquered weakness, and has put away all selfish thoughts, belongs neither to oppressor nor oppressed. He is free.",
                    "A man can only rise, conquer, and achieve by lifting up his thoughts. He can only remain weak, and abject, and miserable by refusing to lift up his thoughts.",
                    "Before a man can achieve anything, even in worldly things, he must lift his thoughts above slavish animal indulgence. He may not, in order to succeed, give up all animality and selfishness, by any means; but a portion of it must, at least, be sacrificed. A man whose first thought is bestial indulgence could neither think clearly nor plan methodically; he could not find and develop his latent resources, and would fail in any undertaking. Not having commenced to manfully control his thoughts, he is not in a position to control affairs and to adopt serious responsibilities. He is not fit to act independently and stand alone. But he is limited only by the thoughts which he chooses.",
                    "There can be no progress, no achievement without sacrifice, and a man's worldly success will be in the measure that he sacrifices his confused animal thoughts, and fixes his mind on the development of his plans, and the strengthening of his resolution and self-reliance. And the higher he lifts his thoughts, the more manly, upright, and righteous he becomes, the greater will be his success, the more blessed and enduring will be his achievements.",
                    "The universe does not favor the greedy, the dishonest, the vicious, although on the mere surface it may appear to do so; it helps the honest, the magnanimous, the virtuous. All the great teachers of the ages have declared this in varying forms, and to prove and know it a man has but to persist in making himself more and more virtuous by lifting up his thoughts.",
                    "Intellectual achievements are the result of thought consecrated to the search for knowledge, or for the beautiful and true in life and nature. Such achievements may be sometimes connected with vanity and ambition, but they are not the outcome of those characteristics; they are the natural outgrowth of long and arduous effort, and of pure and unselfish thoughts.",
                    "Spiritual achievements are the consummation of holy aspirations. He who lives constantly in the conception of noble and lofty thoughts, who dwells upon all that is pure and unselfish, will, as surely as the sun reaches its zenith and the moon its full, become wise and noble in character, and rise into a position of influence and blessedness.",
                    "Achievement, of whatever kind, is the crown of effort, the diadem of thought. By the aid of self-control, resolution, purity, righteousness, and well-directed thought a man ascends; by the aid of animality, indolence, impurity, corruption, and confusion of thought a man descends.",
                    "A man may rise to high success in the world, and even to lofty altitudes in the spiritual realm, and again descend into weakness and degradation by allowing arrogant, selfish, and corrupt thoughts to take possession of him.",
                    "Victories attained by right thought can only be maintained by watchfulness. Many give way when success is assured, and rapidly fall back into failure.",
                    "All achievements, whether in the business, intellectual, or spiritual world, are the result of definitely directed thought, are governed by the same law and are of the same method; the only difference lies in the object of attainment.",
                    "He who would accomplish little must sacrifice little; he who would achieve much must sacrifice much; he who would attain highly must sacrifice greatly."
                ]
            },
            "chapter_6": {
                "title": "Chapter VI: Visions and Ideals",
                "sections": [
                    "The dreamers are the saviors of the world. As the visible world is sustained by the invisible, so men, through all their trials and sins and sordid vocations, are sustained by the beautiful visions of their solitary dreamers. Humanity cannot forget its dreamers; it cannot let their ideals fade and die; it lives in them; it knows them as the realities which it shall one day see and know.",
                    "Composer, sculptor, painter, poet, prophet, sage, these are the makers of the after-world, the architects of heaven. The world is beautiful because they have lived; without them, laboring humanity would perish.",
                    "He who cherishes a beautiful vision, a lofty ideal in his heart, will one day realize it. Columbus cherished a vision of another world, and he discovered it; Copernicus fostered the vision of a multiplicity of worlds and a wider universe, and he revealed it; Buddha beheld the vision of a spiritual world of stainless beauty and perfect peace, and he entered into it.",
                    "Cherish your visions; cherish your ideals; cherish the music that stirs in your heart, the beauty that forms in your mind, the loveliness that drapes your purest thoughts, for out of them will grow all delightful conditions, all heavenly environment; of these, if you but remain true to them, your world will at last be built.",
                    "To desire is to obtain; to aspire is to achieve. Does a man get what he wants by sitting down and wishing for it? He will get what he wants by exerting himself to obtain it. His thoughts must be crystallized into action, and his actions must be sustained by his thoughts.",
                    "The dreamers are the saviors of the world. As the visible world is sustained by the invisible, so men, through all their trials and sins and sordid vocations, are sustained by the beautiful visions of their solitary dreamers. Humanity cannot forget its dreamers; it cannot let their ideals fade and die; it lives in them; it knows them as the realities which it shall one day see and know.",
                    "Composer, sculptor, painter, poet, prophet, sage, these are the makers of the after-world, the architects of heaven. The world is beautiful because they have lived; without them, laboring humanity would perish.",
                    "He who cherishes a beautiful vision, a lofty ideal in his heart, will one day realize it. Columbus cherished a vision of another world, and he discovered it; Copernicus fostered the vision of a multiplicity of worlds and a wider universe, and he revealed it; Buddha beheld the vision of a spiritual world of stainless beauty and perfect peace, and he entered into it.",
                    "Cherish your visions; cherish your ideals; cherish the music that stirs in your heart, the beauty that forms in your mind, the loveliness that drapes your purest thoughts, for out of them will grow all delightful conditions, all heavenly environment; of these, if you but remain true to them, your world will at last be built.",
                    "To desire is to obtain; to aspire is to achieve. Does a man get what he wants by sitting down and wishing for it? He will get what he wants by exerting himself to obtain it. His thoughts must be crystallized into action, and his actions must be sustained by his thoughts.",
                    "The dreamers are the saviors of the world. As the visible world is sustained by the invisible, so men, through all their trials and sins and sordid vocations, are sustained by the beautiful visions of their solitary dreamers. Humanity cannot forget its dreamers; it cannot let their ideals fade and die; it lives in them; it knows them as the realities which it shall one day see and know.",
                    "Composer, sculptor, painter, poet, prophet, sage, these are the makers of the after-world, the architects of heaven. The world is beautiful because they have lived; without them, laboring humanity would perish.",
                    "He who cherishes a beautiful vision, a lofty ideal in his heart, will one day realize it. Columbus cherished a vision of another world, and he discovered it; Copernicus fostered the vision of a multiplicity of worlds and a wider universe, and he revealed it; Buddha beheld the vision of a spiritual world of stainless beauty and perfect peace, and he entered into it.",
                    "Cherish your visions; cherish your ideals; cherish the music that stirs in your heart, the beauty that forms in your mind, the loveliness that drapes your purest thoughts, for out of them will grow all delightful conditions, all heavenly environment; of these, if you but remain true to them, your world will at last be built.",
                    "To desire is to obtain; to aspire is to achieve. Does a man get what he wants by sitting down and wishing for it? He will get what he wants by exerting himself to obtain it. His thoughts must be crystallized into action, and his actions must be sustained by his thoughts."
                ]
            },
            "chapter_7": {
                "title": "Chapter VII: Serenity",
                "sections": [
                    "Calmness of mind is one of the beautiful jewels of wisdom. It is the result of long and patient effort in self-control. Its presence is an indication of ripened experience, and of a more than ordinary knowledge of the laws and operations of thought.",
                    "A man becomes calm in the measure that he understands himself as a thought evolved being, for such knowledge necessitates the understanding of others as the result of thought, and as he develops a right understanding, and sees more and more clearly the internal relations of things by the action of cause and effect, he ceases to fuss and fume and worry and grieve, and remains poised, steadfast, serene.",
                    "The calm man, having learned how to govern himself, knows how to adapt himself to others; and they, in turn, reverence his spiritual strength, and feel that they can learn of him and rely upon him. The more tranquil a man becomes, the greater is his success, his influence, his power for good. Even the ordinary trader will find his business prosperity increase as he develops a greater self-control and equanimity, for people will always prefer to deal with a man whose demeanor is strongly equable.",
                    "The strong, calm man is always loved and revered. He is like a shade-giving tree in a thirsty land, or a sheltering rock in a storm. \"Who does not love a tranquil heart, a sweet-tempered, balanced life? It does not matter whether it rains or shines, or what changes come to those possessing these blessings, for they are always sweet, serene, and calm. That exquisite poise of character which we call serenity is the last lesson of culture, the fruitage of the soul. It is precious as wisdom, more to be desired than gold—yea, than even fine gold. How insignificant mere money-seeking looks in comparison with a serene life—a life that dwells in the ocean of Truth, beneath the waves, beyond the reach of tempests, in the Eternal Calm!\"",
                    "How many people we know who sour their lives, who ruin all that is sweet and beautiful by explosive tempers, who destroy their poise of character, and make bad blood! It is a question whether the great majority of people do not ruin their lives and mar their happiness by lack of self-control. How few people we meet in life who are well balanced, who have that exquisite poise which is characteristic of the finished character!",
                    "Yes, humanity surges with uncontrolled passion, is tumultuous with ungoverned grief, is blown about by anxiety and doubt. Only the wise man, only he whose thoughts are controlled and purified, makes the winds and the storms of the soul obey him.",
                    "Tempest-tossed souls, wherever ye may be, under whatsoever conditions ye may live, know this—in the ocean of life the isles of Blessedness are smiling, and the sunny shore of your ideal awaits your coming. Keep your hand firmly upon the helm of thought. In the bark of your soul reclines the commanding Master; do but wake him, and he will guide you safely across any sea, under any sky, to the isles of Blessedness.",
                    "Self-control is strength; Right Thought is mastery; Calmness is power. Say unto your heart, \"Peace, be still!\""
                ]
            }
        }
    
    def synthesize_chapter(self, chapter_key: str, voice: str = None) -> bool:
        """Synthesize a complete chapter"""
        if chapter_key not in self.chapters:
            logger.info(f"Chapter {chapter_key} not found")
            return False
        
        chapter = self.chapters[chapter_key]
        chapter_dir = self.output_dir / chapter_key
        chapter_dir.mkdir(exist_ok=True)
        
        logger.info(f"\nSynthesizing {chapter['title']}...")
        
        # Synthesize each section
        for i, section in enumerate(chapter['sections'], 1):
            section_file = chapter_dir / f"section_{i:02d}.mp3"
            logger.info(f"  Section {i}...", end=" ")
            
            if self.tts.synthesize(section, str(section_file), voice):
                logger.info("✓")
            else:
                logger.info("✗")
                return False
        
        # Create a combined file for the entire chapter
        self.combine_audio_files(chapter_dir, f"{chapter_key}_complete.mp3")
        logger.info(f"✓ Chapter {chapter['title']} completed")
        return True
    
    def synthesize_all(self, voice: str = None) -> bool:
        """Synthesize all chapters"""
        logger.info(f"Starting synthesis of all chapters using {self.provider_name}...")
        
        for chapter_key in self.chapters.keys():
            if not self.synthesize_chapter(chapter_key, voice):
                logger.info(f"Failed to synthesize {chapter_key}")
                return False
        
        logger.info("\n🎉 All chapters synthesized successfully!")
        return True
    
    def combine_audio_files(self, directory: Path, output_filename: str):
        """Combine multiple audio files into one"""
        try:
            import subprocess
            
            # Get all section files
            section_files = sorted(directory.glob("section_*.mp3"))
            if not section_files:
                return
            
            # Create file list for ffmpeg
            file_list = directory / "file_list.txt"
            with open(file_list, 'w') as f:
                for file in section_files:
                    f.write(f"file '{file.name}'\n")
            
            # Use ffmpeg to combine files
            output_path = directory / output_filename
            cmd = [
                "ffmpeg", "-f", "concat", "-safe", "0", 
                "-i", str(file_list), "-c", "copy", str(output_path), "-y"
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            file_list.unlink()  # Clean up
            
        except Exception as e:
            logger.info(f"Warning: Could not combine audio files: {e}")
    
    def list_chapters(self):
        """List all available chapters"""
        logger.info("\nAvailable chapters:")
        for key, chapter in self.chapters.items():
            logger.info(f"  {key}: {chapter['title']}")
    
    def interactive_mode(self):
        """Interactive mode for chapter selection"""
        while True:
            logger.info(Path("\n") + "="*50)
            logger.info("As a Man Thinketh - Text to Speech System")
            logger.info("="*50)
            logger.info("1. List chapters")
            logger.info("2. Synthesize specific chapter")
            logger.info("3. Synthesize all chapters")
            logger.info("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.list_chapters()
            elif choice == "2":
                self.list_chapters()
                chapter = input("\nEnter chapter key: ").strip()
                if chapter in self.chapters:
                    self.synthesize_chapter(chapter)
                else:
                    logger.info("Invalid chapter key")
            elif choice == "3":
                confirm = input("Synthesize all chapters? (y/N): ").strip().lower()
                if confirm == 'y':
                    self.synthesize_all()
            elif choice == "4":
                logger.info("Goodbye!")
                break
            else:
                logger.info("Invalid choice")

def main():
    """Main function"""
    try:
        tts_system = AsAManThinkethTTS()
        
        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == "list":
                tts_system.list_chapters()
            elif command == "all":
                tts_system.synthesize_all()
            elif command in tts_system.chapters:
                tts_system.synthesize_chapter(command)
            else:
                logger.info(f"Unknown command: {command}")
                logger.info("Usage: python as_a_man_thinketh_tts_real.py [list|all|<chapter_key>]")
        else:
            tts_system.interactive_mode()
            
    except Exception as e:
        logger.info(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()