#!/usr/bin/env python3
"""
Generate a synthetic dataset of activities for the Summer Quest recommendation engine.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any


# Constants
CITIES = [
    "San Diego",
    "La Jolla",
    "Coronado",
    "Del Mar",
    "Carlsbad",
    "Encinitas",
    "Oceanside",
    "Los Angeles",
    "Santa Monica",
    "Pasadena",
    "Irvine",
    "Newport Beach",
    "Laguna Beach",
]

CATEGORIES = [
    "outdoors",
    "food",
    "exercise",
    "creative",
    "social",
    "relaxing",
    "adventure",
    "sightseeing",
    "learning",
    "entertainment",
]

ENERGY_LEVELS = ["low", "medium", "high"]
WEATHER_OPTIONS = ["sunny", "cloudy", "rainy", "any"]

DURATIONS = [1, 2, 3, 4, 5, 6, 8]

# Activity templates organized by type - now detailed descriptions
BEACH_ACTIVITIES = [
    "Take a scenic coastal walk along pristine sandy shores where you can enjoy panoramic ocean views and fresh sea breeze. This peaceful activity is perfect for clearing your mind and appreciating the natural beauty of Southern California's shoreline.",
    "Spend a relaxing day swimming and sunbathing on the sandy beach during summer months. Whether you're looking for a refreshing dip in the ocean or simply want to unwind with a book under an umbrella, the beach offers the perfect escape.",
    "Build elaborate sandcastles and play beach games like frisbee or paddleball with friends and family. These activities are fun for all ages and create wonderful memories while enjoying the sun and surf.",
    "Watch the stunning sunset from the beach as the sky transforms into shades of orange, pink, and purple. This serene experience is ideal for romantic moments, photography, or simply reflecting on your day.",
    "Hunt for shells and sea glass along the shoreline, collecting treasures from the ocean. This meditative activity combines exercise with discovery and is perfect for those who love nature and the ocean's gifts.",
    "Pack a picnic basket and enjoy a meal with an ocean view on the beach. Sharing food and company in such a beautiful natural setting creates a memorable and relaxing experience.",
    "Try paddleboarding or kayaking in the calm waters offshore for a more active beach adventure. These water sports provide excellent exercise while allowing you to explore the marine environment up close.",
    "Explore fascinating tide pools teeming with starfish, sea anemones, and small crustaceans. This educational and low-key activity is perfect for curious explorers of all ages who want to learn about coastal ecosystems.",
    "Organize a beach volleyball game with friends to stay active while enjoying the sand and ocean air. Competitive or casual, this social sport is a great way to get exercise and have fun.",
    "Find a quiet spot on the sand and practice meditation or yoga as waves gently lap against the shore. The rhythmic sound of the ocean creates a naturally peaceful environment for mindfulness and relaxation.",
]

HIKING_ACTIVITIES = [
    "Trek through rugged coastal trails offering breathtaking panoramic views of cliffs, canyons, and the Pacific Ocean. These scenic hikes range from moderate to challenging and are ideal for nature lovers seeking both physical activity and stunning photography opportunities.",
    "Navigate well-maintained forest paths surrounded by native vegetation, wildflowers, and diverse wildlife. Hiking through these natural corridors provides excellent exercise while immersing you in the tranquility of undisturbed nature.",
    "Challenge yourself with a climb to a mountain peak or scenic viewpoint that rewards your effort with expansive vistas. These rewarding hikes are popular among fitness enthusiasts and offer a sense of accomplishment upon reaching the summit.",
    "Discover hidden waterfalls tucked away in canyons and ravines throughout the region. The journey to these natural wonders involves hiking through diverse terrain and often includes opportunities for swimming in refreshing pools.",
    "Spend an afternoon bird watching on marked nature trails where you can spot numerous species in their natural habitats. This peaceful activity combines gentle exercise with the joy of wildlife observation and is perfect for nature enthusiasts.",
    "Follow desert landscape trails featuring unique flora, interesting rock formations, and vast open vistas. These hikes showcase the region's natural diversity and provide a unique perspective on Southern California's ecosystems.",
    "Take a sunrise hike to reach a peak just as dawn breaks, experiencing the magical moment when the landscape transforms with golden light. These early morning adventures offer solitude, beautiful photography opportunities, and a triumphant start to your day.",
    "Explore designated photography trails specifically chosen for their visual appeal and accessibility. These paths allow you to capture stunning natural landscapes and wildlife while enjoying a casual walk through beautiful terrain.",
    "Navigate technical rock scrambling sections that add adventure and challenge to your hiking experience. These more difficult hikes appeal to experienced hikers seeking an adrenaline rush and physical challenge.",
    "Walk through seasonal wildflower blooms that paint entire hillsides in vibrant colors during spring months. This spectacular natural display is perfect for photographers and anyone seeking the beauty of nature at its peak.",
]

FOOD_ACTIVITIES = [
    "Visit a cozy local coffee shop known for handcrafted espresso drinks and artisan pastries. These intimate spaces are perfect for relaxing with a good book, working remotely, or catching up with friends over your favorite beverage.",
    "Dine at a highly-rated restaurant featuring cuisine from award-winning chefs and carefully curated menus. Fine dining experiences offer not just delicious food, but also an opportunity to explore new flavors and culinary techniques.",
    "Browse a farmers market filled with fresh local produce, artisan goods, and homemade specialties from local vendors. These vibrant community gathering spaces offer both high-quality ingredients for cooking and ready-to-eat treats.",
    "Sample authentic street food from food carts and pop-up vendors offering diverse international cuisines. Street food provides an affordable way to explore different cultures through genuine, often family-recipe dishes.",
    "Enjoy wine tasting experiences at local vineyards featuring regional wines and expert sommelier guidance. These tastings often include scenic vineyard locations and pair perfectly with cheese and charcuterie boards.",
    "Participate in a hands-on cooking class where professional chefs teach you techniques and recipes you can recreate at home. These engaging experiences combine learning, creativity, and the reward of eating delicious food you've prepared yourself.",
    "Explore a food festival showcasing local restaurants, food trucks, and culinary artisans all in one location. These lively events offer diverse food options, entertainment, and the chance to discover new favorite restaurants.",
    "Grab authentic tacos from a popular neighborhood taco stand known for quality ingredients and traditional recipes. Quick, affordable, and delicious, these casual meals are beloved by locals and visitors alike.",
    "Enjoy a leisurely brunch at a trendy café featuring creative egg dishes, fresh juices, and specialty coffee drinks. The relaxed brunch atmosphere is perfect for socializing and leisurely starting your weekend.",
    "Indulge in a decadent dessert tasting tour sampling creations from multiple local pastry shops and chocolatiers. This sweet adventure showcases the artistry and skill of local pastry chefs and is perfect for satisfying your sweet tooth.",
]

MUSEUM_ACTIVITIES = [
    "Explore a thought-provoking contemporary art exhibit featuring works from local and international artists. These installations inspire creativity and offer new perspectives on cultural and social issues.",
    "Immerse yourself in abstract and representational art displayed in a world-class gallery setting. Fine art galleries provide opportunities for personal reflection and appreciation of artistic techniques and expressions.",
    "Spend hours in a science museum engaging with interactive exhibits and hands-on demonstrations that explore physics, biology, and technology. These educational experiences make learning fun and accessible for all ages.",
    "Tour a historical museum showcasing artifacts, documents, and exhibits that tell the story of the region's past. Understanding local history enriches your connection to the community and provides valuable cultural education.",
    "Attend a gallery opening reception where artists present their work and mingle with collectors and enthusiasts. These social events combine art appreciation with networking and often feature refreshments and live entertainment.",
    "Explore cultural exhibits celebrating the traditions, art, and history of different communities around the world. These exhibitions promote cross-cultural understanding and appreciation for diverse perspectives.",
    "Admire impressive sculptures and large-scale installations both indoors and in museum gardens. Sculpture exhibits often provide unexpected artistic viewpoints and can be enjoyed at a leisurely pace.",
    "Engage with museum docents who provide expert-guided tours sharing fascinating historical context and artistic significance. These educational tours enhance your understanding and appreciation of the exhibits.",
    "Participate in a museum workshop or educational program designed around current exhibits to deepen your learning. These interactive sessions often include art creation, discussions, or hands-on activities.",
    "Capture stunning photographs of museum collections, architecture, and installations that inspire your artistic eye. Museums provide beautifully lit, carefully curated subjects perfect for photography enthusiasts.",
]

PARK_ACTIVITIES = [
    "Find a peaceful spot in a scenic park surrounded by mature trees and enjoy quality time with nature. Parks provide a natural escape from urban life and offer clean air, shade, and tranquility.",
    "Spread out a blanket and enjoy a home-prepared or takeout meal in a park setting with scenic views. Outdoor picnics combine the pleasure of good food with the beauty of nature and fresh air.",
    "Organize a friendly game of frisbee, badminton, or cornhole with friends and family in a spacious park. These casual outdoor games provide fun, light exercise, and social connection in a beautiful setting.",
    "Visit a botanical garden or community garden to explore carefully planted collections of flowers, shrubs, and trees. These cultivated spaces showcase horticultural artistry and provide inspiration for your own gardening efforts.",
    "Find a comfortable bench or grassy area and spend your afternoon reading a book by a tranquil pond or fountain. The peaceful park environment enhances your reading experience and allows you to absorb nature while enjoying your book.",
    "Set up an easel or bring a sketchbook to capture the beauty of the park's landscape, wildlife, or gardens. Parks provide endless inspiration and peaceful creative environments for artists of all skill levels.",
    "Join a group fitness class or practice yoga and tai chi movements outdoors surrounded by natural scenery. Outdoor exercise combines physical fitness with the therapeutic benefits of fresh air and natural surroundings.",
    "Explore a botanical garden featuring themed areas such as rose gardens, water features, and seasonal plantings. These specialized gardens offer education about plants and provide stunning visual displays throughout the year.",
    "Participate in organized outdoor fitness classes including yoga, Pilates, or high-intensity interval training. Group fitness classes provide structure, motivation, and the social aspect of exercising with others.",
    "Sit quietly with a journal and practice nature journaling by sketching plants, observing wildlife, and recording your observations. This mindful activity combines art, nature appreciation, and personal reflection in one peaceful practice.",
]

SPORT_ACTIVITIES = [
    "Challenge yourself at an indoor or outdoor rock climbing gym featuring climbing walls of varying difficulty levels. This full-body workout builds strength, problem-solving skills, and provides an exhilarating sense of achievement.",
    "Paddle out to catch some waves at a popular local beach break known for reliable swells and friendly surfers. Surfing combines physical challenge, connection with ocean conditions, and a vibrant community of like-minded enthusiasts.",
    "Rally your friends for competitive tennis matches on well-maintained courts at local sports facilities. Tennis provides excellent cardiovascular exercise and is as enjoyable for casual play as it is for serious competition.",
    "Tee off at a scenic local golf course featuring challenging holes and beautiful landscaping set against natural backdrops. Golf offers both physical activity and mental engagement in a leisurely, social setting.",
    "Master skateboarding tricks at a skate park filled with ramps, bowls, and rails designed for all skill levels. This creative sport combines athletic ability with artistic expression and a welcoming community.",
    "Jog along scenic routes through neighborhoods, parks, or trails that offer beautiful views and varying terrain. Running provides excellent cardiovascular fitness and is flexible enough to fit any schedule.",
    "Play full-court basketball games at outdoor courts, testing your skills and enjoying competitive team play. Basketball is a high-energy sport that provides cardiovascular exercise and social interaction.",
    "Cycle through neighborhoods and scenic areas on two-wheeled adventures exploring your local region. Cycling offers freedom, exercise, and the opportunity to discover new places at your own pace.",
    "Swim laps or enjoy recreational swimming at public pools or natural water spots during warmer months. Swimming is an excellent low-impact full-body workout perfect for all fitness levels.",
    "Flow through yoga poses and practice stretching exercises that improve flexibility, strength, and mental clarity. Regular yoga practice builds mind-body connection and promotes overall wellness and relaxation.",
]

COFFEE_SHOP_ACTIVITIES = [
    "Discover a hidden gem coffee shop tucked into a quiet neighborhood corner, known for its cozy atmosphere and skilled baristas. These local spots often feature unique décor, local art, and a welcoming community vibe.",
    "Meet friends or colleagues for coffee and conversation at a café that serves as a comfortable gathering space. Sharing time over coffee strengthens relationships and provides a casual setting for meaningful connection.",
    "Set up your laptop and spend a productive morning or afternoon working remotely from a café with reliable WiFi. Many coffee shops provide the perfect balance of social energy and quiet focus for telecommuters.",
    "Explore a café's menu of specialty coffee drinks crafted with precision and creative flair by expert baristas. Trying different preparations and flavor combinations expands your coffee appreciation and palate.",
    "Find a quiet corner table in a café and spend uninterrupted time studying, reading, or working on personal projects. The subtle background activity and ambient noise in coffee shops often enhances focus for many people.",
    "Chat with friends over espresso drinks in a relaxed café setting where good conversation and quality coffee flow freely. These casual meetups strengthen friendships without the pressure of formal plans.",
    "Participate in a coffee tasting session where experienced baristas guide you through the nuances of different beans and brewing methods. Educational sessions like these deepen your appreciation for coffee quality and craftsmanship.",
    "Attend a café book club meeting to discuss your latest read while sipping your favorite beverage. These community gatherings combine literary discussion with the social warmth of a coffee shop environment.",
    "Learn about specialty coffee preparation methods like pour-over, French press, or AeroPress through hands-on café demonstrations. Understanding different brewing techniques helps you appreciate the complexity of coffee production.",
    "Settle in with a warm beverage and enjoy the calming ritual of sipping coffee while watching the world go by through café windows. This simple pleasure provides a meditative break from daily stress.",
]

MARKET_ACTIVITIES = [
    "Wake up early and browse a local farmer's market filled with seasonal produce, flowers, and artisan goods directly from producers. These vibrant community gathering spaces support local agriculture while offering fresh, high-quality ingredients.",
    "Wander through an outdoor marketplace exploring vendor stalls offering everything from handmade crafts to ethnic foods. These bustling markets provide cultural immersion, unique shopping experiences, and opportunities to discover new products.",
    "Hunt for fresh produce and locally-made specialties at a market that prioritizes quality and sustainability. Shopping at farmers markets supports local businesses and provides nutritious ingredients for healthy home cooking.",
    "Browse beautiful handmade crafts including jewelry, ceramics, textiles, and art pieces created by local artisans. Craft markets showcase local talent and offer one-of-a-kind items with stories and authenticity.",
    "Support local producers by shopping directly for fresh fruits, vegetables, honey, and artisan products at market stalls. Direct producer-to-consumer sales ensure quality and provide a personal connection to your food sources.",
    "Sample offerings from street vendors showcasing international cuisines and local specialties throughout a bustling market. Markets are adventure playgrounds for food lovers seeking authentic flavors and exciting new experiences.",
    "Search through vintage and antique vendors at a market to discover treasured items with history and character. Antique shopping combines treasure hunting with appreciation for craftsmanship and design of bygone eras.",
    "Attend a lively craft fair or maker market showcasing local artists, crafters, and entrepreneurs selling their creations. These events celebrate creativity and provide direct artist engagement while supporting small businesses.",
    "Explore a night market during evening hours when the atmosphere becomes especially festive and vibrant. Evening markets often feature entertainment, special vendors, and a more relaxed social atmosphere.",
    "Purchase locally-sourced goods and discover new products from passionate vendors committed to quality and sustainability. Supporting local makers and farmers builds community connections and strengthens the local economy.",
]

CLASS_ACTIVITIES = [
    "Unleash your creativity by taking a painting or pottery class where instructors guide you through techniques and artistic expression. These hands-on classes are perfect for beginners and encourage personal artistic discovery.",
    "Learn photography fundamentals including composition, lighting, and camera settings in an informative and practical workshop. Photography classes help you develop a photographer's eye and improve your ability to capture beautiful images.",
    "Move to music in a dynamic dance class that teaches choreography while providing excellent cardiovascular exercise. Dance classes combine physical fitness with creative expression and offer a fun, social workout environment.",
    "Strengthen your body and build endurance in a structured fitness class including options like HIIT, pilates, or aerobics. Group fitness classes provide motivation, expert instruction, and the energy of exercising alongside peers.",
    "Develop musical skills and learn to play an instrument with guidance from experienced musicians in one-on-one or group settings. Music lessons open creative outlets and provide the satisfaction of mastering a new skill.",
    "Explore the digital world and build practical coding skills through beginner-friendly computer programming classes. Coding classes prepare you for technical career opportunities or simply expand your problem-solving abilities.",
    "Communicate more effectively in a new language through immersive language classes taught by native speakers. Language learning opens cultural doors and provides practical skills for travel and international communication.",
    "Deepen your practice in a yoga or stretching workshop focusing on flexibility, strength, and mindfulness. These specialized classes often explore specific yoga styles or address particular physical goals.",
    "Build confidence and practical self-defense skills in a dedicated martial arts or self-defense class. These empowering classes provide fitness benefits, personal safety knowledge, and mental resilience.",
    "Master sailing techniques and water navigation skills in an introductory sailing class on local waterways. Sailing classes provide thrilling outdoor experiences while teaching valuable maritime knowledge.",
]

BOOKSTORE_ACTIVITIES = [
    "Spend hours browsing a local independent bookstore filled with carefully curated selections and knowledgeable staff recommendations. Independent bookstores provide personalized service and often host author events and book clubs.",
    "Attend an author reading and book signing event where writers share their work and interact personally with readers. These literary events provide insights into the creative process and foster direct author-reader connections.",
    "Discover thoughtful book recommendations from bookstore staff and other readers who are passionate about literature. Personal recommendations often lead to unexpected literary treasures that match your interests perfectly.",
    "Join a vibrant book club that gathers regularly to discuss current and classic titles in a collaborative community setting. Book clubs combine literary analysis with friendship and provide accountability for reading goals.",
    "Search through bins and shelves of rare, signed, and vintage books at specialty bookstores catering to collectors. Book collectors appreciate the hunt for special editions and the history contained in older volumes.",
    "Settle into a café corner within a bookstore and lose yourself in reading while sipping coffee and enjoying snacks. Bookstore cafés create the perfect atmosphere for leisurely reading and literary immersion.",
    "Attend intimate poetry readings where local and visiting poets share their work in a literary atmosphere. Poetry events celebrate the rhythm and beauty of language and create meaningful connections among literature enthusiasts.",
    "Hunt for first editions and signed copies of books that hold special significance for your personal collection. The thrill of finding a rare edition makes the collector's journey rewarding and exciting.",
    "Participate in book-related events including author talks, themed parties, and literary discussions hosted regularly at bookstores. These community gatherings celebrate literature and build relationships among fellow book lovers.",
    "Exchange book recommendations with fellow readers and build your reading list with personalized suggestions from experts and peers. Community engagement at bookstores enriches your reading life and exposes you to diverse perspectives.",
]

DAY_TRIP_ACTIVITIES = [
    "Plan a morning drive to nearby charming towns and villages, exploring local shops, restaurants, and cultural attractions. Day trips to neighboring communities offer the diversity of travel without requiring time off or overnight accommodations.",
    "Hike to a scenic overlook offering expansive views of the landscape, coastline, or valleys that inspire and captivate. Viewpoints reward the journey with vistas that showcase the region's natural beauty.",
    "Venture out to explore a neighboring city's unique neighborhoods, attractions, and cultural offerings different from your hometown. Experiencing nearby urban centers broadens your perspective and reveals hidden gems.",
    "Spend the day at a local theme park enjoying thrilling rides, family attractions, and carnival food with friends or family. Theme parks provide entertainment, excitement, and the festive atmosphere of carefree fun.",
    "Visit a wildlife sanctuary to observe animals in naturalistic settings while learning about conservation efforts. Sanctuaries offer ethical animal encounters combined with education about endangered species and habitat protection.",
    "Explore caves and caverns featuring dramatic rock formations, underground passages, and geological wonders. Cave exploration combines adventure with earth science education and creates memorable experiences.",
    "Celebrate special occasions by attending seasonal festivals featuring food, entertainment, music, and cultural performances. Festivals bring communities together and offer immersive cultural and entertainment experiences.",
    "Tour a winery situated on scenic hillsides, learning about wine production through tastings and educational presentations. Winery visits combine learning, beautiful landscapes, and the social pleasure of wine appreciation.",
    "Soak in natural hot springs nestled in scenic areas, combining relaxation with the therapeutic benefits of mineral-rich waters. Hot springs offer a unique wellness experience in natural outdoor settings.",
    "Visit iconic landmarks and famous sites that define the region's identity, offering photo opportunities and cultural significance. Landmark visits provide touchstones to local history and identity while creating lasting memories.",
]

PHOTOGRAPHY_ACTIVITIES = [
    "Wake up early to photograph the magical golden hour light that transforms landscapes into warm, glowing scenes. Golden hour photography sessions reward early risers with naturally beautiful lighting conditions.",
    "Explore cityscapes on foot, capturing architectural details, street life, and urban landscapes from fresh perspectives. Urban photography celebrates the character and energy of built environments while developing your artistic eye.",
    "Trek through natural areas with your camera to capture wildlife in natural habitats and stunning landscape vistas. Nature photography combines hiking with creative expression and teaches patience and observation skills.",
    "Focus on capturing sweeping landscapes featuring mountains, valleys, coastlines, or other grand natural features. Landscape photography encourages exploration of beautiful locations while developing compositional skills.",
    "Venture into urban streets with a camera, capturing candid moments of daily life and interesting subjects in spontaneous situations. Street photography documents the human experience and creates compelling visual narratives.",
    "Coordinate a photography walk with fellow enthusiasts exploring a neighborhood or natural area and sharing techniques. Group photo walks combine social connection with shared learning and mutual inspiration.",
    "Get close to capture detailed images of flowers, insects, and other small subjects using macro photography techniques. Macro photography reveals hidden beauty in everyday items and trains your eye for detail.",
    "Join a structured photography workshop led by experienced photographers who teach composition, light, and technical skills. Workshops accelerate learning and provide personalized feedback on your photographic development.",
    "Search for and photograph Instagram-worthy locations and trending spots that showcase the region's photogenic qualities. Social media photography encourages exploration and creative interpretation of beautiful places.",
    "Rise before sunrise to photograph the moment when dawn light breaks across the landscape in stunning colors and patterns. Sunrise photography sessions offer the reward of witnessing nature's most beautiful light show.",
]

VOLUNTEER_ACTIVITIES = [
    "Join organized beach cleanup efforts removing trash and plastic debris from shorelines to protect marine ecosystems. Beach cleanups combine environmental stewardship with community service and the satisfaction of visible impact.",
    "Dedicate your day to volunteering at local charities serving various causes from food banks to homeless shelters. Volunteer work provides meaningful contribution to causes you believe in while building community connections.",
    "Help at an animal shelter caring for rescued animals, walking dogs, and socializing cats and other creatures. Animal shelter volunteering provides rewarding work for animal lovers while supporting essential rescue services.",
    "Participate in community garden projects growing fresh produce for local food banks and community members. Community gardens combine gardening activity with food security efforts and neighborhood connection.",
    "Support food bank operations by sorting, organizing, and distributing donated food to families in need. Food banking efforts directly address food insecurity while building understanding of community needs.",
    "Assist at community centers offering educational programs and services to underserved populations. Community center volunteering helps provide resources and opportunities to those who need them most.",
    "Help maintain trails through clearing brush, removing fallen trees, and improving trail conditions for public use. Trail maintenance volunteers directly enhance outdoor recreation opportunities while caring for natural spaces.",
    "Tutor students in academic subjects including reading, math, science, and writing through formal or informal programs. Tutoring provides direct educational support while building mentoring relationships with young people.",
    "Participate in ecological restoration projects replanting native species and removing invasive plants from natural areas. Restoration volunteering repairs ecosystems while deepening understanding of environmental conservation.",
    "Contribute your skills at local museums and cultural institutions providing visitor services and educational programs. Museum volunteering supports cultural institutions while sharing knowledge and enriching community access to arts and history.",
]

NAME_PREFIXES = [
    "Morning",
    "Evening",
    "Weekend",
    "Relaxing",
    "Adventure",
    "Solo",
    "Group",
    "Hidden",
    "Local",
    "Popular",
    "Scenic",
    "Fun",
    "Unique",
    "Best",
    "New",
]

NAME_ACTIVITY_TYPES = [
    "Beach Walk",
    "Hiking Trail",
    "Restaurant",
    "Café",
    "Museum",
    "Park",
    "Workout",
    "Surf Session",
    "Bike Ride",
    "Class",
    "Market",
    "Gallery",
    "Theater",
    "Festival",
    "Bookshop",
    "Yoga Session",
    "Rock Climbing",
    "Photography Tour",
    "Cooking Experience",
    "Dance Class",
    "Meditation",
    "Picnic",
    "Kayaking",
    "Shopping",
]

# Map activity types to templates
ACTIVITY_TYPES = {
    "Beach": (BEACH_ACTIVITIES, ["outdoors", "relaxing", "social", "sightseeing"], ["sunny", "cloudy", "any"]),
    "Hiking": (HIKING_ACTIVITIES, ["outdoors", "exercise", "adventure", "sightseeing"], ["sunny", "cloudy"]),
    "Food": (FOOD_ACTIVITIES, ["food", "social", "entertainment"], ["any"]),
    "Museum": (MUSEUM_ACTIVITIES, ["learning", "entertainment", "sightseeing", "creative"], ["any"]),
    "Park": (PARK_ACTIVITIES, ["outdoors", "relaxing", "exercise", "social"], ["sunny", "cloudy", "any"]),
    "Sport": (SPORT_ACTIVITIES, ["exercise", "adventure", "social"], ["sunny", "cloudy"]),
    "Coffee": (COFFEE_SHOP_ACTIVITIES, ["food", "social", "relaxing", "entertainment"], ["any"]),
    "Market": (MARKET_ACTIVITIES, ["food", "social", "sightseeing", "shopping"], ["sunny", "any"]),
    "Class": (CLASS_ACTIVITIES, ["creative", "learning", "exercise", "entertainment"], ["any"]),
    "Bookstore": (BOOKSTORE_ACTIVITIES, ["learning", "relaxing", "entertainment", "social"], ["any"]),
    "Day Trip": (DAY_TRIP_ACTIVITIES, ["adventure", "sightseeing", "entertainment"], ["sunny", "cloudy", "any"]),
    "Photography": (PHOTOGRAPHY_ACTIVITIES, ["creative", "outdoor", "sightseeing", "learning"], ["sunny", "cloudy"]),
    "Volunteer": (VOLUNTEER_ACTIVITIES, ["social", "relaxing", "learning", "outdoors"], ["any"]),
}





def generate_duration() -> int:
    """Generate a realistic activity duration."""
    return random.choice(DURATIONS)


def get_weather_for_category(category: str) -> List[str]:
    """Get appropriate weather options for a category."""
    weather_map = {
        "outdoors": ["sunny", "cloudy", "any"],
        "food": ["any"],
        "exercise": ["sunny", "cloudy", "any"],
        "creative": ["any"],
        "social": ["any"],
        "relaxing": ["sunny", "cloudy", "any"],
        "adventure": ["sunny", "cloudy"],
        "sightseeing": ["sunny", "cloudy", "any"],
        "learning": ["any"],
        "entertainment": ["any"],
    }
    options = weather_map.get(category, ["any"])
    num_options = random.randint(1, len(options))
    return random.sample(options, num_options)


def generate_activity(activity_id: int, activity_type: str) -> Dict[str, Any]:
    """Generate a single activity with all required fields."""
    templates, category_pool, weather_pool = ACTIVITY_TYPES[activity_type]
    
    description = random.choice(templates)
    category = random.choice(category_pool)
    city = random.choice(CITIES)
    energy = random.choice(ENERGY_LEVELS)
    weather = random.sample(weather_pool, k=random.randint(1, len(weather_pool)))
    
    activity = {
        "id": activity_id,
        "city": city,
        "category": category,
        "duration_hours": generate_duration(),
        "weather": weather,
        "energy": energy,
        "description": description,
    }
    
    return activity


def generate_dataset(num_activities: int = None) -> List[Dict[str, Any]]:
    """Generate a complete dataset of unique activities."""
    if num_activities is None:
        num_activities = random.randint(1000, 2000)
    
    activities = []
    activity_id = 1
    
    # Ensure variety by rotating through activity types
    activity_types = list(ACTIVITY_TYPES.keys())
    
    for i in range(num_activities):
        # Cycle through activity types for variety
        activity_type = activity_types[i % len(activity_types)]
        activity = generate_activity(activity_id, activity_type)
        
        activity["id"] = activity_id
        activities.append(activity)
        activity_id += 1
    
    return activities


def save_dataset(activities: List[Dict[str, Any]], filepath: Path) -> None:
    """Save the dataset to a JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(activities, f, indent=2)
    
    print(f"✓ Saved {len(activities)} activities to {filepath}")


def main():
    """Generate and save the activity dataset."""
    output_path = Path(__file__).parent.parent.parent / "data" / "activities.json"
    
    print("Generating activity dataset...")
    activities = generate_dataset()
    
    print(f"Generated {len(activities)} unique activities")
    save_dataset(activities, output_path)
    
    # Show sample activities
    print("\n📋 Sample activities:")
    print("-" * 80)
    for activity in activities[:5]:
        print(f"\nID: {activity['id']}")
        print(f"City: {activity['city']}")
        print(f"Category: {activity['category']}")
        print(f"Duration: {activity['duration_hours']} hours")
        print(f"Weather: {', '.join(activity['weather'])}")
        print(f"Energy: {activity['energy']}")
        print(f"Description: {activity['description']}")
    
    # Statistics
    print("\n" + "=" * 80)
    print("📊 Dataset Statistics:")
    print("=" * 80)
    print(f"Total activities: {len(activities)}")
    
    categories = {}
    for activity in activities:
        cat = activity["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nActivities by category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    
    cities = {}
    for activity in activities:
        city = activity["city"]
        cities[city] = cities.get(city, 0) + 1
    
    print(f"\nActivities by city:")
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
        print(f"  {city}: {count}")


if __name__ == "__main__":
    main()
