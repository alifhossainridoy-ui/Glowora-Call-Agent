#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Product Database for Cosmetics
Pre-populated with common cosmetics products
"""

from cosmetics.product_brain import Product, CosmeticsProductBrain


def create_sample_database() -> CosmeticsProductBrain:
    """Create sample product database"""

    brain = CosmeticsProductBrain()

    sample_products = [
        Product(
            id="FC001",
            name="Glow Brightening Facial Cream",
            name_bn="গ্লো ব্রাইটেনিং ফেসিয়াল ক্রিম",
            category="Facial Cream",
            price=450.0,
            stock=25,
            description="Brightening facial cream with vitamin C and niacinamide for radiant skin",
            description_bn="ভিটামিন সি এবং নায়াসিনামাইড সহ ব্রাইটেনিং ফেসিয়াল ক্রিম উজ্জ্বল ত্বকের জন্য",
            ingredients=["Vitamin C", "Niacinamide", "Hyaluronic Acid", "Aloe Vera", "Glycerin"],
            skin_types=["normal", "combination", "oily"],
            concerns=["dark_spot", "dullness"],
            usage="Apply on cleansed face morning and night",
            usage_bn="পরিষ্কার মুখে সকাল ও রাতে লাগান",
            warnings="Patch test before use. Avoid eye area.",
            warnings_bn="ব্যবহারের আগে প্যাচ টেস্ট করুন। চোখের এড়িয়ে লাগান।",
            brand="Glow Beauty", size="50ml", rating=4.5, reviews_count=128
        ),
        Product(
            id="SR002",
            name="Anti-Aging Retinol Serum",
            name_bn="অ্যান্টি-এজিং রেটিনল সিরাম",
            category="Serum",
            price=890.0,
            stock=15,
            description="Powerful retinol serum for reducing fine lines and wrinkles",
            description_bn="ফাইন লাইন এবং রিংকল কমাতে শক্তিশালী রেটিনল সিরাম",
            ingredients=["Retinol", "Peptides", "Hyaluronic Acid", "Vitamin E"],
            skin_types=["normal", "dry", "combination"],
            concerns=["wrinkle", "aging"],
            usage="Use at night. Start with 2-3 times per week",
            usage_bn="রাতে ব্যবহার করুন। সপ্তাহে ২-৩ বার দিয়ে শুরু করুন",
            warnings="Use sunscreen during day. Not for sensitive skin.",
            warnings_bn="দিনে সানস্ক্রিন ব্যবহার করুন। সেনসিটিভ স্কিনের জন্য নয়।",
            brand="Ageless", size="30ml", rating=4.7, reviews_count=256
        ),
        Product(
            id="SS003",
            name="SPF 50 Sunscreen Gel",
            name_bn="এসপিএফ ৫০ সানস্ক্রিন জেল",
            category="Sunscreen",
            price=380.0,
            stock=40,
            description="Lightweight gel sunscreen with broad spectrum protection",
            description_bn="হালকা জেল সানস্ক্রিন ব্রড স্পেকট্রাম প্রোটেকশন সহ",
            ingredients=["Zinc Oxide", "Titanium Dioxide", "Aloe Vera", "Green Tea Extract"],
            skin_types=["oily", "combination", "sensitive"],
            concerns=["sun_protection", "oily"],
            usage="Apply 15 minutes before sun exposure. Reapply every 2 hours",
            usage_bn="রোদে যাওয়ার ১৫ মিনিট আগে লাগান। প্রতি ২ ঘণ্টায় রিঅ্যাপ্লাই করুন",
            warnings="Reapply after swimming or sweating",
            warnings_bn="সাঁতার বা ঘামের পর রিঅ্যাপ্লাই করুন",
            brand="SunGuard", size="60ml", rating=4.3, reviews_count=89
        ),
        Product(
            id="MC004",
            name="Hydrating Moisturizer",
            name_bn="হাইড্রেটিং ময়েশ্চারাইজার",
            category="Moisturizer",
            price=320.0,
            stock=30,
            description="Deep hydrating moisturizer for dry and sensitive skin",
            description_bn="শুষ্ক এবং সেনসিটিভ ত্বকের জন্য গভীর হাইড্রেটিং ময়েশ্চারাইজার",
            ingredients=["Hyaluronic Acid", "Ceramides", "Shea Butter", "Squalane"],
            skin_types=["dry", "sensitive", "normal"],
            concerns=["dryness", "sensitivity"],
            usage="Apply on cleansed face morning and night",
            usage_bn="পরিষ্কার মুখে সকাল ও রাতে লাগান",
            warnings="For external use only",
            warnings_bn="শুধু বাহ্যিক ব্যবহারের জন্য",
            brand="HydraCare", size="100ml", rating=4.6, reviews_count=312
        ),
        Product(
            id="CL005",
            name="Gentle Foaming Cleanser",
            name_bn="জেন্টল ফোমিং ক্লিনজার",
            category="Cleanser",
            price=280.0,
            stock=35,
            description="Gentle foaming cleanser for all skin types",
            description_bn="সব ত্বকের ধরনের জন্য জেন্টল ফোমিং ক্লিনজার",
            ingredients=["Salicylic Acid", "Tea Tree Oil", "Chamomile", "Glycerin"],
            skin_types=["oily", "combination", "normal"],
            concerns=["acne", "oily"],
            usage="Wet face, apply cleanser, massage gently, rinse",
            usage_bn="মুখ ভিজিয়ে ক্লিনজার লাগিয়ে আলতো করে ম্যাসাজ করুন, ধুয়ে ফেলুন",
            warnings="Avoid contact with eyes",
            warnings_bn="চোখে লাগাবেন না",
            brand="PureClean", size="150ml", rating=4.4, reviews_count=178
        ),
        Product(
            id="LP006",
            name="Matte Liquid Lipstick",
            name_bn="ম্যাট লিকুইড লিপস্টিক",
            category="Lipstick",
            price=350.0,
            stock=50,
            description="Long-lasting matte liquid lipstick in 12 shades",
            description_bn="১২টি শেডে দীর্ঘস্থায়ী ম্যাট লিকুইড লিপস্টিক",
            ingredients=["Isododecane", "Dimethicone", "Vitamin E", "Jojoba Oil"],
            skin_types=["all"],
            concerns=["makeup"],
            usage="Apply on lips. Let dry for 30 seconds",
            usage_bn="ঠোঁটে লাগান। ৩০ সেকেন্ড শুকতে দিন",
            warnings="Discontinue if irritation occurs",
            warnings_bn="জ্বালা হলে ব্যবহার বন্ধ করুন",
            brand="LipGlam", size="5ml", rating=4.2, reviews_count=445
        ),
        Product(
            id="PF007",
            name="Rose Gold Perfume",
            name_bn="রোজ গোল্ড পারফিউম",
            category="Perfume",
            price=1200.0,
            stock=20,
            description="Elegant rose gold perfume with floral notes",
            description_bn="ফ্লোরাল নোট সহ এলিগেন্ট রোজ গোল্ড পারফিউম",
            ingredients=["Rose Extract", "Jasmine", "Musk", "Vanilla"],
            skin_types=["all"],
            concerns=["fragrance"],
            usage="Spray on pulse points",
            usage_bn="পালস পয়েন্টে স্প্রে করুন",
            warnings="Keep away from fire",
            warnings_bn="আগুন থেকে দূরে রাখুন",
            brand="ScentLux", size="100ml", rating=4.8, reviews_count=67
        ),
        Product(
            id="BL008",
            name="Cocoa Butter Body Lotion",
            name_bn="কোকো বাটার বডি লোশন",
            category="Body Lotion",
            price=290.0,
            stock=45,
            description="Rich cocoa butter body lotion for smooth skin",
            description_bn="মসৃণ ত্বকের জন্য সমৃদ্ধ কোকো বাটার বডি লোশন",
            ingredients=["Cocoa Butter", "Shea Butter", "Vitamin E", "Almond Oil"],
            skin_types=["dry", "normal"],
            concerns=["dryness", "roughness"],
            usage="Apply all over body after shower",
            usage_bn="গোসলের পর সারা শরীরে লাগান",
            warnings="External use only",
            warnings_bn="শুধু বাহ্যিক ব্যবহার",
            brand="BodySoft", size="400ml", rating=4.5, reviews_count=234
        ),
        Product(
            id="HC009",
            name="Argan Oil Hair Serum",
            name_bn="আর্গান অয়েল হেয়ার সিরাম",
            category="Hair Care",
            price=520.0,
            stock=18,
            description="Nourishing argan oil serum for damaged hair",
            description_bn="ক্ষতিগ্রস্ত চুলের জন্য পুষ্টিকর আর্গান অয়েল সিরাম",
            ingredients=["Argan Oil", "Keratin", "Vitamin B5", "Silk Protein"],
            skin_types=["all"],
            concerns=["hair_damage", "frizz"],
            usage="Apply on damp hair, focus on ends",
            usage_bn="ভেজা চুলে লাগান, আগায় বেশি করে",
            warnings="Avoid scalp if oily",
            warnings_bn="তেলতেলে হলে স্কাল্পে লাগাবেন না",
            brand="HairLux", size="100ml", rating=4.6, reviews_count=189
        ),
        Product(
            id="FM010",
            name="Charcoal Face Mask",
            name_bn="চারকোল ফেস মাস্ক",
            category="Face Mask",
            price=180.0,
            stock=60,
            description="Deep cleansing charcoal face mask for pore purification",
            description_bn="পোর পরিষ্কারের জন্য ডিপ ক্লিনজিং চারকোল ফেস মাস্ক",
            ingredients=["Activated Charcoal", "Bentonite Clay", "Tea Tree Oil", "Witch Hazel"],
            skin_types=["oily", "combination"],
            concerns=["acne", "pores", "oily"],
            usage="Apply on cleansed face, leave 15-20 min, rinse",
            usage_bn="পরিষ্কার মুখে লাগান, ১৫-২০ মিনিট রাখুন, ধুয়ে ফেলুন",
            warnings="Use 1-2 times per week only",
            warnings_bn="সপ্তাহে ১-২ বার ব্যবহার করুন",
            brand="PureDetox", size="50ml", rating=4.3, reviews_count=156
        )
    ]

    for product in sample_products:
        brain.add_product(product)

    print(f"Added {len(sample_products)} sample products")
    return brain


if __name__ == '__main__':
    db_brain = create_sample_database()

    print("\nRecommendations for oily skin with acne:")
    for p in db_brain.recommend(skin_type='oily', concern='acne'):
        print(f"  - {p.name} (TK{p.price})")
