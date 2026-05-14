from pymem import Pymem

PVZ_memory = Pymem()
PVZ_pid = 0
PVZ_version = "Game not found"
zombies_HP_addresses = None
plant_size = 304
zombie_size = 304


def update_PVZ_memory(memory):
    global PVZ_memory, plant_size, zombie_size
    PVZ_memory = memory
    try:
        plant_size = PVZ_memory.read_uint(0x41C965)
        zombie_size = PVZ_memory.read_uint(0x41C905)
    except:  # noqa: E722
        plant_size = 304
        zombie_size = 304


def update_PVZ_pid(pid):
    global PVZ_pid
    PVZ_pid = pid


def update_PVZ_version(version):
    global PVZ_version
    global zombies_HP_addresses
    PVZ_version = version
    zombies_HP_addresses = get_zombies_HP_addresses(PVZ_version)
    print(PVZ_version)


baseAddress = 0x006A9EC0

zombiesType = [
    "Normal Zombie",
    "Flag Zombie",
    "Conehead Zombie",
    "Pole Vaulting Zombie",
    "Buckethead Zombie",
    "Ice Cart Bro",
    "Screen Door Zombie",
    "Black Olive Zombie",
    "Armed Disco Zombie",
    "Backup Dancer",
    "Inner Tube Normal Zombie",
    "Snorkel Zombie",
    "Ice Cart Gargantuar",
    "Zomboni",
    "Dolphin Gatling Zombie",
    "Jack in the Box Zombie",
    "Balloon Disco Zombie",
    "Digger Zombie",
    "Pogo Zombie",
    "Ice Cart Yeti",
    "Bungee Zombie",
    "Ladder Zombie",
    "Catapult Zombie",
    "Gargantuar",
    "Imp",
    "Dr. Zomboss",
    "Pea Zombie",
    "Wall-nut Zombie",
    "Jalapeno Zombie",
    "Gatling Zombie",
    "Ice Squash Zombie",
    "High Ice Fruit Zombie",
    "Gargantuar (Red Eye)",
    "Disco Zombie",
    "Dancer Zombie",
    "Skeleton Zombie",
    "Necromancer",
    "Fire Disco Zombie",
    "Fire Dancer",
    "Rubber Ducky Zombie",
    "Bed Cart Zombie",
    "Small Fall Guy Zombie",
    "Olive Giant",
    "Olive Imp",
    "Yeti Digger Zombie",
    "Wild Gatling Zombie",
    "Torch Nut Zombie",
    "Gatling Pole Vaulting Zombie",
    "Gatling Dolphin Zombie",
    "Zombie Nut Giant",
    "Zombie Pea Imp",
    "Shark Zombie",
    "Ice Shooter Zombie",
    "Siren Zombie",
    "Tangle Snorkel Zombie",
    "Diamond Zombie",
    "Blast Door Zombie",
    "Duck Rider Zombie",
    "Cart Imp Zombie",
    "Jar Zombie",  # 59
    "Hypnotist Zombie",  # 60
    "Gardener Zombie",  # 61
    "Red Eye Disco Zombie",  # 62
    "Giant Backup Dancer",  # 63
    "Shadow Zombie",  # 64
    "Digger Spikeweed Imp",  # 65
    "Charge Black Olive Red Eye Giant Zombie",  # 66
    "Charge Black Olive Red Eye Imp",  # 67
    "Red Eye Ice Cart Zombie",  # 68
    "Double Cactus Zombie",  # 69
    "Box Nut Zombie",  # 70
    "VIP Nut Zombie",  # 71
    "Threepeater Corn Zombie",  # 72
    "Frost Giant Zombie",  # 73
    "Edgar Jr.",  # 74
    "Gatling Ice Cart Zombie",  # 75
    "Jammer Car Zombie",  # 76
    "Sunflower Zombie",  # 77
    "Farmer Zombie",  # 78
    "Rich Man Zombie",  # 79
    "Disco Dance Zombie",  # 80
    "Dance Backup Dancer Zombie",  # 81
    "Ice Catapult Zombie",  # 82
    "Ghost Zombie",  # 83
    "Imitater Zombie",  # 84
    "Treant Zombie",  # 85
    "Zombie Bug",  # 86
    "Olive Pole Vaulting Zombie",  # 87
    "Digger Giant Zombie",  # 88
    "Digger Imp Zombie",  # 89
    "Pirate Captain Zombie",  # 90
    "Pirate Crew Zombie",  # 91
    "Magnetic Field Zombie",  # 92
    "Snail Imp Zombie",  # 93
    "Cat Warrior Zombie",  # 94
    "Balloon Cart Zombie",  # 95
    "Football Yeti Zombie",  # 96
    "Rebirth Mage Zombie",  # 97
    "Yeti Sled Zombie Squad",  # 98
    "Armed Sled Zombie Member",  # 99
    "Vampire Zombie",  # 100
    "Checkers Zombie",  # 101
    "Monkey Zombie",  # 102
    "Market Zombie",  # 103
    "Angel Zombie",  # 104
    "Newspaper Disco Zombie",  # 105
    "Angry Dancer Zombie",  # 106
    "Snorkel Dolphin Zombie",  # 107
    "Disco Dolphin Zombie",  # 108
    "Backup Dolphin Zombie",  # 109
    "Jack-in-the-Box Pole Vaulting Zombie",  # 110
    "Smoke Machine Zombie",  # 111
    "Imp Catapult Zombie",  # 112
    "Christmas Gift Box Zombie",  # 113
    "Balloon Ladder Zombie",  # 114
    "Gift Box Gargantuar",  # 115
    "Gift Box Imp Zombie",  # 116
    "Lottery Box Zombie",  # 117
    "Skeleton Gargantuar",  # 118
    "Skeleton Imp Zombie",  # 119
    "Gardening Cart Zombie",  # 120
    "Giant Airship",  # 121
    "Balloon Imp Zombie",  # 122
    "Wild Ice Cart Giant Zombie",  # 123
    "Wild Gargantuar",  # 124
    "High Ice Fruit Imp Zombie",  # 125
    "Christmas Treant Zombie",  # 126
    "Diamond Gargantuar",  # 127
    "Diamond Imp Zombie",  # 128
    "White Swan Zombie",  # 129
    "Gift Box Machine Zombie",  # 130
    "Super Gatling Shooter Zombie",  # 131
    "VIP Nut Gargantuar",  # 132
    "VIP Nut Imp Zombie",  # 133
    "Magnetic Jammer Car Zombie",  # 134
    "Ghost Jack-in-the-Box Zombie",  # 135
    "Angel Gargantuar",  # 136
    "Sunflower Queen Zombie",  # 137
    "Fire Sunflower Dancer Zombie",  # 138
]
zombieSpaw = zombiesType + [
    "Green Cone Probability",
    "Olive Draft Helmet Probability",
    "Disco Draft Helmet Probability",
    "Giant Draft Helmet Probability",
]
itemType = [
    "Unknown 0",
    "Tombstone",
    "Crater",
    "Ladder",
    "Blue Portal",
    "White Portal",
    "Unknown 6",
    "Vase",
    "Unknown 8",
    "Unknown 9",
    "Snail",
    "Rake",
    "Brain",
    "Unknown 13",
    "Unknown 14",
    "Rubber Ducky",
]
shovelType = [
    "Normal Shovel",  # 0
    "Silver Shovel",  # 1
    "Gold Shovel",  # 2
    "Diamond Shovel",  # 3
    "Star Shovel",  # 4
    "Ice Shovel",  # 5
    "Jalapeno Shovel",  # 6
    "Skeleton Shovel",  # 7
    "Cyclone Shovel",  # 8
    "Pumpkin Shovel",  # 9
    "Gift Box Shovel",  # 10
    "Charm Shovel",  # 11
    "Burger Shovel",  # 12
    "Luxury Shovel",  # 13
    "Card Shovel",  # 14
    "Wisdom Shovel",  # 15
]
plantsType = [
    "PeaSunflower",  # 0
    "Sun Bean",  # 1
    "Sun Bomb",  # 2
    "Torch Nut",  # 3
    "Sun Potato Mine",  # 4
    "Ice Cattail",  # 5
    "Garlic Flower",  # 6
    "Double Cactus",  # 7
    "Small Pot Mushroom",  # 8
    "Sun Sunflower",  # 9
    "Ice Melon Fume-shroom",  # 10
    "Tomb Mine Layer",  # 11
    "Red Eye Mushroom",  # 12
    "Sun Scaredy-shroom",  # 13
    "Snow Ice-shroom",  # 14
    "Charm Doom-shroom",  # 15
    "Pea Lily Pad",  # 16
    "Ice Squash",  # 17
    "Pea Wishing Well",  # 18
    "Doom Seaweed",  # 19
    "Chermander",  # 20
    "Butter Spikeweed",  # 21
    "Ice Torchwood",  # 22
    "High Ice Fruit",  # 23
    "Sea Nut",  # 24
    "No. 6 Lamp Flower",  # 25
    "Pea Cannon",  # 26
    "Cactus Clover",  # 27
    "Taco Cattail",  # 28
    "Spikeweed Starfruit",  # 29
    "Gloom Pumpkin",  # 30
    "Magnet Nut",  # 31
    "Gatling Cabbage-pult",  # 32
    "Sun Flower Pot",  # 33
    "Threepeater Corn",
    "Random Plant Box",
    "Charm Garlic",
    "Coffee Umbrella",
    "Cactus Clover Flower",
    "Watermelon Nut",
    "Burger Shooter",
    "Sun Pumpkin Palm",
    "Butter Gloom-shroom",
    "Watermelon Cattail",
    "Sun-shroom Pult",
    "Marigold Magnet",
    "Steel Thorn Nut King",
    "Doom Cannon",
    "Imitater",
    "Explosion Nut",
    "Giant Nut",
    "Sprout",
    "(Reverse) Double Cactus",
    "<null>",
    "Fire",  # 54
    "Weiweimi",  # 55
    "Call Net Admin",  # 56
    "Friendly Screen Door Zombie",  # 57
    "Gloom-shroom Pult Bullet",  # 58
    "No. 6 Lamp Flower Deathrattle",  # 59
    "Ultimate Shooter",  # 60
    "Sunflower Princess",  # 61
    "Burger King",  # 62
    "Cola (Attack Speed x2)",  # 63
    "Fries (HP x2)",  # 64
    "Pumpkin Cannon Bullet",  # 65
    "Flower Pot",  # 66
    "Lily Pad",  # 67
    "Seven Color Flower",  # 68
    "Tengteng Travel Clover",  # 69
    "Spikeweed Bullet",  # 70
    "Melon Seed",  # 71
    "Blast Door Zombie (Friendly)",  # 72
    "Starfruit",  # 73
    "Red Envelope",  # 74
    "Firecracker Mine",
    "Firecracker Nut Wall",
    "Pea Cattail",
    "Ice Melon Cattail",
    "Blazing Pumpkin",
    "Zombie Peashooter",
    "Ice Clover",
    "Hot Dog Shooter",
    "Ice Cactus",
    "Shadow Squash King",
    "Butter JOKER",
    "Sunflower Queen",
    "Garlic Jalapeno",
    "VIP Nut",
    "Zombie Nut Wall",
    "Charm-shroom Shooter",
    "Fortune Marigold",
    "Cat Litter Box",
    "Crater Nut",
    "Bouncy Fume-shroom",
    "Ice Spikeweed",
    "Earth Starfruit",
    "Elf Mushroom",
    "Sichuan Cuisine Pult",
    "Nut Imitater",
    "Squash Nut",
    "Frozen Nut",
    "Brainstorm",
    "Treasure Devourer",
    "Hologram Card Projector",
    "Growth Coffee Bean",
    "Cold Light Mushroom",
    "Scorching Peashooter",
    "Fluorescent Mallet",
    "Wild Gatling Shooter",
    "Life Reshaper",
    "Twin Cherries",
    "Lucky Clover",
    "Gold Sunflower",
    "Potato Cannon",
    "Punishment Cage",
    "Reserve Supplies",
    "Spikeweed Chomper",
    "Zombie Bean",
    "Forbidden Doom-shroom",
    "Match-3 Candy",
    "Sea Ice-shroom",
    "Lotus Shell",
    "Kitty Sunflower",
    "Gift Box Machine",
    "Fortune Cat",
    "Crystal Snail",
    "Nut Piggy Bank",
    "Gold Magnet Shooter",
    "Diamond Seed",
    "Lottery Box Deluxe",
    "Prismatic Starfruit",
    "Nut Bowling",
    "Evolution Bean",
    "Meteor",
    "Apple Alarm Clock",
    "Sea Pea",
    "Pea Seaweed",
    "Ocean Star",
    "Box Nut",
    "Bait Mushroom",
    "Flower Pot Lily Pad",
    "Gloom-shroom Pult",
    "Injured Sunflower",
    "Medical Coffee Bean",
    "Injured Fume-shroom",
    "Ice Cannon",
    "Gold Watermelon Pult",
    "Ice-shroom King",
    "Self-Funded Box",
    "Involution Pult",
    "Ice Maker Bean",
    "Disguised Sunflower",
    "Scorching Corn Pult",
    "Jalapeno Reshaper",
    "Prism Sunflower",
    "King Steel Tooth Flower",
    "Promotion Bean",
    "Promotion Nut",
    "Promotion Flower Pot",
    "Angel Sunflower",
    "Recycle Tall-nut",  # 161
    "Rainbow Candy",  # 162
    "Transform Tall-nut",  # 163
    "Reverse Alarm Clock",  # 164
    "Sun Cannon",  # 165
    "Forbidden Ice-shroom",  # 166
    "Ice Fire Splitter",  # 167
    "Pea Bomb",  # 168
    "Jalapeno Sun-shroom",  # 169
    "Pea Pod Shell",  # 170
    "Gloom Coffee Bean",  # 171
    "Fried Egg",  # 172
    "Chilly Fume-shroom",  # 173
    "Ice Flame Pumpkin",  # 174
    "VIP Stump",  # 175
    "Soul Bean",  # 176
    "Star Box",  # 177
    "Cat Bed",  # 178
    "Gold Hammer",  # 179
    "Wheel Reshaper",  # 180
    "Psychedelic Pult",  # 181
    "Corn Spinner",  # 182
    "Thunder Fruit",  # 183
    "Bowling Egg",  # 184
    "Leaf Tall-nut",  # 185
    "Watermelon Fume-shroom",  # 186
    "Pumpkin Cannon",  # 187
    "Small Puff-shroom Pult",  # 188
    "Taco Mortar",  # 189
    "Torch Jalapeno",  # 190
    "Zombie Sunflower ",  # 191
    "Big Mouth Sun-shroom",  # 192
    "Flower Pot Lily Pad",  # 193
    "Gatling Flower Pot",  # 194
    "Sea Mushroom",  # 195
    "Coffee Clover",  # 196
    "Zombie Cannon",  # 197
    "Sun Charm-shroom",  # 198
    "Tomb Breaker",  # 199
    "Torch Umbrella",  # 200
    "Spikeweed Umbrella",  # 201
    "Magnet Potato Mine",  # 202
    "Spikeweed Watermelon Pult",  # 203
    "Magnet Spikeweed King",  # 204
    "Jack-o'-Lantern",  # 205
    "Card Imitater",  # 206
    "Blazing Doom-shroom",  # 207
    "Jungle Bulk Pea",  # 208
    "Torch Jalapeno Bean",  # 209
    "Forbidden Coffee Bean",  # 210
    "Pumpkin Pult",  # 211
    "Pumpkin Box",  # 212
    "Nut Sunflower",  # 213
    "Ice Bomb",  # 214
    "Starfruit Threepeater",  # 215
    "Tangle Rush",  # 216
    "Ice Torch Charm-shroom",  # 217
    "Potato Squash Mine",  # 218
    "Cherry Bean",  # 219
    "Starfruit Stump",  # 220
    "Ghost Charm-shroom",  # 221
    "Mini Burger Shooter",  # 222
    "Baptized Threepeater",  # 223
    "Cat Star Gatling",  # 224
    "Submarine Fireworks",  # 225
    "Appreciation Bean",  # 226
    "Sunflower",  # 227
    "Peashooter",  # 228
    "Wall-nut",  # 229
    "Cherry Bomb",  # 230
    "Coffee Cat",  # 231
    "Big Mouth Gatling Shooter",  # 232
    "Diamond Nut",  # 233
    "Marigold",  # 234
    "Zombie Torchwood",  # 235
    "Charm Lamp Flower",  # 236
    "Starfruit Magnet-shroom",  # 237
    "Cherry Corn Pult",  # 238
    "Charm Seaweed",  # 239
    "Zombie Spikeweed",  # 240
    "Spike Ball Bullet",  # 241
    "Garlic Threepeater",  # 242
    "Cherry Fume-shroom",  # 243
    "Fertilizer Tall-nut",  # 244
    "Snail Chomper",  # 245
    "Chocolate Nut",  # 246
    "Trolley Flower Pot",  # 247
    "Chocolate",  # 248
    "Cabbage Artillery",  # 249
    "Fortune Stump",  # 250
    "Pesticide Fume-shroom",  # 251
    "Golden Sunflower",  # 252
    "Glove Bean",  # 253
    "Cornucopia",  # 254
    "Record Player Scaredy-shroom",  # 255
    "Watering Can Pult",  # 256
    "Cherry Potato Mine",  # 257
    "Garlic Tall-nut",  # 258
    "Jalapeno Pesticide",  # 259
    "Reshape Fertilizer",  # 260
    "Key Coffee Bean",  # 261
    "Squash Gloom-shroom",  # 262
    "Starfruit Umbrella",  # 263
    "Healing Flower Pot",  # 264
    "Cherry Gold Magnet",  # 265
    "Injured Tall-nut",  # 266
    "Bandage Nut Cannon",  # 267
    "Clover Chomper",  # 268
    "Magic Box",  # 269
    "Firecracker Double Shooter",  # 270
    "Mini Ice-shroom",  # 271
    "Tangle Mine",  # 272
    "Pumpkin Trash Can",  # 273
    "Broom Coffee Bean",  # 274
    "Nut Pumpkin Head",  # 275
    "Spike Pumpkin Head",  # 276
    "Flag Zombie Bean",  # 277
    "Garlic Bomb",  # 278
    "Garlic Gas",  # 279
    "Scorching Cactus",  # 280
    "Scale Coffee Bean",  # 281
    "Galaxy Starfruit",  # 282
    "Zombie Gatling Shooter",  # 283
    "Ice Magnet-shroom",  # 284
    "Ice Bean",  # 285
    "Arctic Ice Melon Pult",  # 286
    "Spikeweed Flower Pot",  # 287
    "Pumpkin Umbrella",  # 288
    "Gloom Charm-shroom",  # 289
    "Magnet Corn Pult",  # 290
    "Charge Magnet",  # 291
    "Nut Umbrella",  # 292
    "Charm Box",  # 293
    "Youwang Cloud Ground Cleaner",  # 294
    "Arctic Ice-shroom",  # 295
    "Garlic Flower Pot",  # 296
    "Scaredy Sun-shroom",  # 297
    "Tangle Lily Pad",  # 298
    "Clover Fume-shroom",  # 299
    "Snow Lotus",  # 300
    "Cat Tail Umbrella",  # 301
    "Clover Potato Mine",  # 302
    "Jack-in-the-Box Magnet-shroom",  # 303
    "Jack-in-the-Box",  # 304
    "Random Imitater",  # 305
    "Cat Tail Clover",  # 306
    "Jack-in-the-Box Pumpkin Head",  # 307
    "Potato Scaredy-shroom",  # 308
    "Magnet Cherry Bomb",  # 309
    "Tangle Seaweed Nut",  # 310
    "Tangle Seaweed Ball",  # 311
    "Star Magnet",  # 312
    "Magnet Clover",  # 313
    "Splitter Stump",  # 314
    "Giant Nut Bowling",  # 315
    "Explosive Nut",  # 316
    "Latte Game",  # 317
    "Big Mouth Corn Crab",  # 318
    "Ice Chomper",  # 319
    "Ice-shroom Shooter",  # 320
    "Rake",  # 321
    "Cyber Surge Skin",  # 322
    "Idol Singer Skin",  # 323
    "Western Sheriff Skin",  # 324
    "Summer Drink Skin",  # 325
    "Holiday Cool Skin",  # 326
    "Sun Lamp Flower",  # 327
    "Ice Sunflower",  # 328
    "Scaredy Doom-shroom",  # 329
    "Forbidden Flower Pot",  # 330
    "Doom Mine",  # 331
    "Charm Spikeweed",  # 332
    "Potato Threepeater",  # 333
    "Clover Sunflower",  # 334
    "Watermelon Shed",  # 335
    "Love Guardian Skin",  # 336
    "Candy Platter Skin",  # 337
    "Water Basin",  # 338
    "Sun Torchwood",  # 339
    "Squash Shell",  # 340
    "Lamp Doom-shroom",  # 341
    "Lamp Doom-shroom Lighting",  # 342
    "Lamp Doom-shroom Aura",  # 343
    "Sun Doom-shroom",  # 344
    "Wild Puff-shroom",  # 345
    "Promotion Burger Shooter",  # 346
    "Bubble Stump",  # 347
    "Doom Sunflower",  # 348
    "Super Gatling Shooter",  # 349
    "Super Burger Gatling Shooter",  # 350
    "Super Zombie Gatling Shooter",  # 351
    "Super Wild Gatling Shooter",  # 352
    "Cactus Point Defense Cannon",  # 353
    "Super Ice Cactus Gatling Shooter",  # 354
    "Wild Sniper Shooter",  # 355
    "Super Sunflower Gatling Shooter",  # 356
    "Nut Cactus",  # 357
]
if isinstance(PVZ_version, (int, float)) and PVZ_version < 3.4:
    for _ in range(len(plantsType), 256):
        plantsType.append("Placeholder")
else:
    for _ in range(len(plantsType), 512):
        plantsType.append("Placeholder")
plantsType = plantsType + [
    "Normal Zombie",
    "Flag Zombie",
    "Conehead Zombie",
    "Pole Vaulting Zombie",
    "Buckethead Zombie",
    "Ice Cart Bro",
    "Screen Door Zombie",
    "Black Olive Zombie",
    "Armed Disco Zombie",
    "Backup Dancer",
    "Inner Tube Normal Zombie",
    "Snorkel Zombie",
    "Ice Cart Giant",
    "Zomboni",
    "Dolphin Pea Knight",
    "Jack in the Box Zombie",
    "Balloon Disco Zombie",
    "Digger Zombie",
    "Pogo Zombie",
    "Ice Cart Yeti",
    "Bungee Zombie",
    "Ladder Zombie",
    "Catapult Zombie",
    "Gargantuar",
    "Imp",
    "Dr. Zomboss",
    "Pea Zombie",
    "Wall-nut Zombie",
    "Jalapeno Zombie",
    "Gatling Zombie",
    "Ice Squash Zombie",
    "High Ice Fruit Zombie",
    "Gargantuar (Red Eye)",
    "Disco Zombie",
    "Dancer Zombie",
    "Skeleton Zombie",
    "Necromancer",
    "Fire Disco Zombie",
    "Fire Dancer",
    "Rubber Ducky Zombie",
    "Bed Cart Zombie",
    "Small Fall Guy Zombie",
    "Olive Giant",
    "Olive Imp",
    "Yeti Digger Zombie",
    "Wild Gatling Zombie",
    "Torch Nut Zombie",
    "Gatling Pole Vaulting Zombie",
    "Gatling Dolphin Zombie",
    "Zombie Nut Giant",
    "Zombie Pea Imp",
    "Shark Zombie",
    "Ice Shooter Zombie",
    "Siren Zombie",
    "Tangle Snorkel Zombie",
    "Diamond Zombie",
    "Blast Door Zombie",
    "Duck Rider Zombie",
    "Cart Imp Zombie",
    "Jar Zombie",  # 315
    "Hypnotist Zombie",  # 316
    "Gardener Zombie",  # 317
    "Red Eye Disco Zombie",  # 318
    "Giant Backup Dancer",  # 319
    "Shadow Zombie",  # 320
    "Digger Spikeweed Imp",  # 321
    "Charge Black Olive Red Eye Giant Zombie",  # 322
    "Charge Black Olive Red Eye Imp",  # 323
    "Red Eye Ice Cart Zombie",  # 324
    "Double Cactus Zombie",  # 325
    "Box Nut Zombie",  # 326
    "VIP Nut Zombie",  # 327
    "Threepeater Corn Zombie",  # 328
    "Frost Giant Zombie",  # 329
    "Edgar Jr.",  # 330
    "Gatling Ice Cart Zombie",  # 331
    "Jammer Car Zombie",  # 332
    "Sunflower Zombie",  # 333
    "Farmer Zombie",  # 334
    "Rich Man Zombie",  # 335
    "Disco Dance Zombie",  # 336
    "Dance Backup Dancer Zombie",  # 337
    "Ice Catapult Zombie",  # 338
    "Ghost Zombie",  # 339
    "Imitater Zombie",  # 340
    "Treant Zombie",  # 341
    "Zombie Bug",  # 342
    "Olive Pole Vaulting Zombie",  # 343
    "Digger Giant Zombie",  # 344
    "Digger Imp Zombie",  # 345
    "Pirate Captain Zombie",  # 346
    "Pirate Crew Zombie",  # 347
    "Magnetic Field Zombie",  # 348
    "Snail Imp Zombie",  # 349
    "Cat Warrior Zombie",  # 350
    "Balloon Cart Zombie",  # 351
    "Football Yeti Zombie",  # 608
    "Rebirth Mage Zombie",  # 609
    "Yeti Sled Zombie Squad",  # 610
    "Armed Sled Zombie Member",  # 611
    "Vampire Zombie",  # 612
    "Checkers Zombie",  # 613
    "Monkey Zombie",  # 614
    "Market Zombie",  # 615
    "Angel Zombie",  # 616
    "Newspaper Disco Zombie",  # 617
    "Angry Dancer Zombie",  # 618
    "Snorkel Dolphin Zombie",  # 619
    "Disco Dolphin Zombie",  # 620
    "Backup Dolphin Zombie",  # 621
    "Jack-in-the-Box Pole Vaulting Zombie",  # 622
    "Smoke Machine Zombie",  # 623
    "Imp Catapult Zombie",  # 624
    "Christmas Gift Box Zombie",  # 625
    "Balloon Ladder Zombie",  # 626
    "Gift Box Gargantuar",  # 627
    "Gift Box Imp Zombie",  # 628
    "Lottery Box Zombie",  # 629
    "Skeleton Gargantuar",  # 630
    "Skeleton Imp Zombie",  # 631
    "Gardening Cart Zombie",  # 632
    "Giant Airship",  # 633
    "Balloon Imp Zombie",  # 634
    "Wild Ice Cart Giant Zombie",  # 635
    "Wild Gargantuar",  # 636
    "High Ice Fruit Imp Zombie",  # 637
    "Christmas Treant Zombie",  # 638
    "Diamond Gargantuar",  # 639
    "Diamond Imp Zombie",  # 640
    "White Swan Zombie",  # 641
    "Gift Box Machine Zombie",  # 642
    "Super Gatling Shooter Zombie",  # 643
    "VIP Nut Gargantuar",  # 644
    "VIP Nut Imp Zombie",  # 645
    "Magnetic Jammer Car Zombie",  # 646
    "Ghost Jack-in-the-Box Zombie",  # 647
    "Angel Gargantuar",  # 648
    "Sunflower Queen Zombie",  # 649
    "Fire Sunflower Dancer Zombie",  # 650
]

ExcludedPutCards = [
    "Sun Bean",
    "Tomb Mine Layer",
    "Pea Lily Pad",
    "Doom Seaweed",
    "Random Plant Box",
    "Doom Cannon",
    "Treasure Devourer",
    "Hologram Card Projector",
    "Growth Coffee Bean",
    "Fluorescent Mallet",
    "Life Reshaper",
    "Lucky Clover",
    "Gold Sunflower",
    "Potato Cannon",
    "Reserve Supplies",
    "Zombie Bean",
    "Lotus Shell",
    "Lottery Box Deluxe",
    "Nut Bowling",
    "Evolution Bean",
    "Medical Coffee Bean",
    "Ice Cannon",
    "Gold Watermelon Pult",
    "Self-Funded Box",
    "Ice Maker Bean",
    "Promotion Bean",
    "Sun Bean",
    "Coffee Umbrella",
    "Pea Wishing Well",
    "Angel Sunflower",
    "Sun Cannon",
    "Life Reshaper",
    "Gold Hammer",  # 179
    "Torch Jalapeno Bean",  # 209
    "Forbidden Coffee Bean",  # 210
    "Appreciation Bean",  # 226
]
DownPlantCards = [
    "Small Pot Mushroom",
    "Sun Flower Pot",
    "Cat Litter Box",
    "Flower Pot Lily Pad",
    "Promotion Flower Pot",
    "Fried Egg",  # 172
    "Gloom Coffee Bean",  # 171
    "Cat Bed",  # 178
    "Flower Pot Lily Pad",  # 193
    "Gatling Flower Pot",  # 194
]
PumpkinPlantCards = [
    "Gloom Pumpkin",
    "Sun Pumpkin Palm",
    "Blazing Pumpkin",
    "Ice Flame Pumpkin",  # 174
    "Jack-o'-Lantern",  # 205
]
AshPlantCards = [
    "Sun Bomb",
    "Snow Ice-shroom",
    "Charm Doom-shroom",
    "Chermander",
    "Cactus Clover",
    "Ice Clover",
    "Butter JOKER",
    "Garlic Jalapeno",
    "Charm-shroom Shooter",
    "Brainstorm",
    "Cold Light Mushroom",
    "Twin Cherries",
    "Punishment Cage",
    "Forbidden Doom-shroom",
    "Match-3 Candy",
    "Meteor",
    "Apple Alarm Clock",
    "Ice-shroom King",
    "Jalapeno Reshaper",
    "Rainbow Candy",
    "Reverse Alarm Clock",
    "Forbidden Ice-shroom",
    "Pea Bomb",  # 168
    "Soul Bean",  # 176
    "Wheel Reshaper",  # 180
    "Torch Jalapeno",  # 190
    "Coffee Clover",  # 196
    "Tomb Breaker",  # 199
    "Ice Bomb",  # 214
    "Cherry Bean",  # 219
]


def get_zombies_HP_addresses(PVZ_version):
    print("PVZ_version", PVZ_version)
    if PVZ_version == 2.0:
        return {
            "Normal Zombie": 0x005227BB,
            "Conehead's Cone": 0x522892,
            "Conehead's Green Cone": 0x0085A8AF,
            "Pole Vaulting Zombie": 0x522CBF,
            "Pole Vaulting Zombie's Nut": 0x0085AA02,
            "Buckethead's Bucket": 0x52292B,
            "Newspaper": 0x52337D,
            "Ice Cart Bro": 0x0085ADCD,
            "Screen Door's Door": 0x522949,
            "Screen Door's Cone": 0x0085A0CD,
            "Screen Door's Bucket": 0x0085A080,
            "Black Olive's Black Olive Hat": 0x522BB0,
            "Black Olive's Draft Helmet": 0x85A794,
            "Disco Zombie": 0x523530,
            "Disco Zombie's Black Olive Hat": 0x0085A501,
            "Disco Zombie's Draft Helmet": 0x0085A56D,
            "Snorkel & Catapult's Black Olive Hat": 0x0085A025,
            "Large Ice Cart": 0x522DE1,
            "Zomboni": 0x523139,
            "Zombo Squad": 0x0085AB94,
            "Dolphin Zombie": 0x522D64,
            "Dolphin's Cone": 0x0085A6FD,
            "Jack in the Box Zombie": 0x522FC7,
            "Jack in the Box's Cone": 0x0085A0EA,
            "Balloon Zombie": 0x005234BF,
            "Digger's Olive Hat": 0x522BEF,
            "Digger Body": 0x0085A6C3,
            "Pogo Zombie": 0x523300,
            "Pogo's Bucket": 0x0085A1EC,
            "Pogo's Nut": 0x0085A326,
            "Ice Cart Yeti": 0x52296E,
            "Bungee Zombie": 0x522A1B,
            "Ladder Body and Ladder": 0x52299C,
            "Ladder's Cone": 0x0085A347,
            "Ladder's Bucket": 0x0085A39E,
            "Ladder's Nut": 0x0085A4E0,
            "Catapult Zombie": 0x522E8D,
            "Gargantuar (White Eye)": 0x523D26,
            "Gargantuar (Red Eye)": 0x523E4A,
            "Gargantuar's Door": 0x0085A5CE,
            "Gargantuar's Bucket": 0x0085A5BA,
            "Gargantuar's Black Olive Hat": 0x0085A6B0,
            "Gargantuar's Draft Helmet": 0x0085A656,
            "Plant Zombie's Door": 0x0085A1C6,
            "Plant Zombie's Cone": 0x0085A1A4,
            "Plant Zombie's Bucket": 0x0085A156,
            "Wall-nut Zombie's Nut": 0x52382B,
            "Jalapeno Zombie's Jalapeno": 0x523A87,
            "High Ice Fruit Zombie's High Ice Fruit": 0x52395D,
            "Disco Zombie": 0x0085A82D,
            "Skeleton": 0x0085AB76,
            "Necromancer": 0x0085ADB2,
            "Fire Disco Zombie": 0x0085AC14,
            "Fire Dancer": 0x0085AD96,
            "Bed Cart": 0x0085AE77,
            "Small Fall Guy's Sleep Cap": 0x0085AEC7,
            "Rubber Ducky's Cone": 0x0085AE63,
            "Rubber Ducky's Bucket": 0x0085AE30,
            "Dr. Zomboss": 0x0085AEE5,
        }
    elif PVZ_version == 2.1 or PVZ_version == 2.2:
        return {
            "Normal Zombie": 0x005227BB,
            "Conehead's Cone": 0x00522892,
            "Conehead's Green Cone": 0x008D08AF,
            "Conehead's Green Cone Max": 0x008D08B9,
            "Pole Vaulting Zombie": 0x00522CBF,
            "Pole Vaulting Zombie's Nut": 0x008D0A02,
            "Buckethead's Bucket": 0x0052292B,
            "Newspaper": 0x0052337D,
            "Ice Cart Bro": 0x008D0DCD,
            "Screen Door's Door": 0x00522949,
            "Screen Door's Cone": 0x008D00CD,
            "Screen Door's Bucket": 0x008D0080,
            "Black Olive's Black Olive Hat": 0x00522BB0,
            "Black Olive's Draft Helmet": 0x008D0794,
            "Black Olive's Draft Helmet Max": 0x008D079E,
            "Disco Zombie": 0x00523530,
            "Disco Zombie's Black Olive Hat": 0x008D0501,
            "Disco Zombie's Draft Helmet": 0x008D056D,
            "Disco Zombie's Draft Helmet Max": 0x008D0577,
            "Snorkel & Catapult's Black Olive Hat": 0x008D0025,
            "Large Ice Cart": 0x00522DE1,
            "Zomboni": 0x00523139,
            "Zombo Squad": 0x008D0B94,
            "Zombo Squad Max": 0x008D0B9E,
            "Jack in the Box Zombie": 0x00522FC7,
            "Jack in the Box's Cone": 0x008D00EA,
            "Balloon Zombie": 0x005234BF,
            "Digger Body": 0x008D06C3,
            "Pogo Zombie": 0x00523300,
            "Pogo's Bucket": 0x008D01EC,
            "Pogo's Nut": 0x008D0326,
            "Ice Cart Yeti": 0x0052296E,
            "Bungee Zombie": 0x00522A1B,
            "Ladder Body and Ladder": 0x0052299C,
            "Ladder Zombie's Cone Accessory": 0x008D0347,
            "Ladder's Cone": 0x008D039E,
            "Ladder's Nut": 0x008D04E0,
            "Catapult Zombie": 0x00522E8D,
            "Gargantuar (White Eye)": 0x00523D26,
            "Gargantuar (Red Eye)": 0x00523E4A,
            "Gargantuar's Door": 0x008D05CE,
            "Gargantuar's Bucket": 0x008D05BA,
            "Gargantuar's Black Olive Hat": 0x008D06B0,
            "Gargantuar's Draft Helmet": 0x008D0656,
            "Gargantuar's Draft Helmet Max": 0x008D0660,
            "Plant Zombie's Door": 0x008D01C6,
            "Plant Zombie's Cone": 0x008D01A4,
            "Plant Zombie's Bucket": 0x008D0156,
            "Wall-nut Zombie's Nut": 0x0052382B,
            "Jalapeno Zombie's Jalapeno": 0x00523A87,
            "High Ice Fruit Zombie's High Ice Fruit": 0x0052395D,
            "Disco Zombie": 0x008D082D,
            "Skeleton": 0x008D0B76,
            "Skeleton Max": 0x008D0B80,
            "Necromancer": 0x008D0DB2,
            "Fire Disco Zombie": 0x008D0C14,
            "Fire Dancer": 0x008D0D96,
            "Bed Cart": 0x008D0E77,
            "Small Fall Guy's Sleep Cap": 0x008D0EC7,
            "Small Fall Guy's Sleep Cap Max": 0x008D0ED1,
            "Rubber Ducky's Cone": 0x008D0E63,
            "Rubber Ducky's Bucket": 0x008D0E30,
            "Dr. Zomboss": 0x008D0EE5,
            "Olive Giant": 0x008D0F04,
            "Olive Giant Helmet": 0x008D0F18,
            "Olive Imp Helmet": 0x008D0F8F,
            "Yeti Digger Zombie": 0x008D0FA3,
            "Yeti Digger Hat": 0x008D0FC9,
        }
    elif PVZ_version == 2.3:
        return {
            "Normal Zombie": 0x005227BB,
            "Conehead's Cone": 0x00522892,
            "Conehead's Green Cone": 0x008D08AA,
            "Pole Vaulting Zombie": 0x00522CBF,
            "Pole Vaulting Zombie's Nut": 0x008D09FD,
            "Buckethead's Bucket": 0x0052292B,
            "Newspaper": 0x0052337D,
            "Ice Cart Bro": 0x008D0DAE,
            "Screen Door's Door": 0x00522949,
            "Screen Door's Cone": 0x008D00CD,
            "Screen Door's Bucket": 0x008D0080,
            "Black Olive's Black Olive Hat": 0x00522BB0,
            "Black Olive's Draft Helmet": 0x008D078F,
            "Disco Zombie": 0x00523530,
            "Disco Zombie's Black Olive Hat": 0x008D04E5,
            "Disco Zombie's Draft Helmet": 0x008D0551,
            "Snorkel & Catapult's Black Olive Hat": 0x008D0025,
            "Large Ice Cart": 0x00522DE1,
            "Zomboni": 0x00523139,
            "Zombo Squad": 0x008D0B75,
            "Dolphin Zombie": 0x00522D64,
            "Dolphin's Cone": 0x008D06E1,
            "Jack in the Box Zombie": 0x00522FC7,
            "Jack in the Box's Cone": 0x008D00EA,
            "Balloon Zombie": 0x005234BF,
            "Digger Body": 0x008D06A7,
            "Pogo Zombie": 0x00523300,
            "Pogo's Bucket": 0x008D01EC,
            "Pogo's Nut": 0x008D0318,
            "Ice Cart Yeti": 0x0052296E,
            "Bungee Zombie": 0x00522A1B,
            "Ladder Body and Ladder": 0x0052299C,
            "Ladder Zombie's Bucket": 0x008D0390,
            "Ladder's Cone": 0x008D0339,
            "Ladder's Nut": 0x008D04C4,
            "Catapult Zombie": 0x00522E8D,
            "Catapult Olive Hat": 0x008D0025,
            "Gargantuar (White Eye)": 0x00523D26,
            "Gargantuar (Red Eye)": 0x00523E4A,
            "Gargantuar's Door": 0x008D05B2,
            "Gargantuar's Bucket": 0x008D059E,
            "Gargantuar's Black Olive Hat": 0x008D0694,
            "Gargantuar's Draft Helmet": 0x008D063A,
            "Imp": 0x005227BB,
            "Plant Zombie Body": 0x005227BB,
            "Plant Zombie's Door": 0x008D01C6,
            "Plant Zombie's Cone": 0x008D01A4,
            "Plant Zombie's Bucket": 0x0052292B,
            "Wall-nut Zombie's Nut": 0x0052382B,
            "Jalapeno Zombie's Jalapeno": 0x00523A87,
            "High Ice Fruit Zombie's High Ice Fruit": 0x008D11D1,
            "Gatling Shooter Zombie": 0x008D11A2,
            "Torch Nut Zombie's Nut Head": 0x008D12EC,
            "Gatling Pole Vaulting Zombie": 0x008D1415,
            "Gatling Dolphin Zombie's Cone": 0x008D164F,
            "Disco Zombie": 0x008D0828,
            "Skeleton": 0x008D0B57,
            "Necromancer": 0x008D0D93,
            "Fire Disco Zombie": 0x008D0BF5,
            "Fire Dancer": 0x008D0D77,
            "Bed Cart": 0x008D0E58,
            "Small Fall Guy's Sleep Cap": 0x008D0EA8,
            "Rubber Ducky's Cone": 0x008D0E44,
            "Rubber Ducky's Bucket": 0x008D0E11,
            "Dr. Zomboss": 0x008D0EC6,
            "Olive Giant": 0x008D0F01,
            "Olive Giant Helmet": 0x008D0F15,
            "Olive Imp": 0x005227BB,
            "Olive Imp Helmet": 0x008D0F8C,
            "Yeti Digger Zombie": 0x008D0FC6,
            "Yeti Digger Hat": 0x008D0FA0,
            "Diamond Zombie Hat": 0x008D1DF7,
            "Shark Zombie": 0x008D1A97,
            "Siren Zombie": 0x008D1C4D,
            "Tangle Snorkel Zombie": 0x008D1CDA,
        }
    elif PVZ_version == 2.35 or PVZ_version >= 2.36:
        return {
            "Normal Zombie": 0x005227BB,
            "Conehead's Cone": 0x00522892,
            "Conehead's Green Cone": 0x008D08AA,
            "Pole Vaulting Zombie": 0x00522CBF,
            "Pole Vaulting Zombie's Nut": 0x008D09FD,
            "Buckethead's Bucket": 0x0052292B,
            "Newspaper": 0x0052337D,
            "Ice Cart Bro": 0x008D0DAE,
            "Screen Door's Door": 0x00522949,
            "Screen Door's Cone": 0x008D00CD,
            "Screen Door's Bucket": 0x008D0080,
            "Black Olive's Black Olive Hat": 0x00522BB0,
            "Black Olive's Draft Helmet": 0x008D078F,
            "Disco Zombie": 0x00523530,
            "Disco Zombie's Black Olive Hat": 0x008D04E5,
            "Disco Zombie's Draft Helmet": 0x008D0551,
            "Snorkel & Catapult's Black Olive Hat": 0x008D0025,
            "Large Ice Cart": 0x00522DE1,
            "Zomboni": 0x00523139,
            "Zombo Squad": 0x008D0B75,
            "Dolphin Zombie": 0x00522D64,
            "Dolphin's Cone": 0x008D06E1,
            "Jack in the Box Zombie": 0x00522FC7,
            "Jack in the Box's Cone": 0x008D00EA,
            "Balloon Zombie": 0x005234BF,
            "Digger Body": 0x008D06A7,
            "Pogo Zombie": 0x00523300,
            "Pogo's Bucket": 0x008D01EC,
            "Pogo's Nut": 0x008D0318,
            "Ice Cart Yeti": 0x0052296E,
            "Bungee Zombie": 0x00522A1B,
            "Ladder Body and Ladder": 0x0052299C,
            "Ladder Zombie's Bucket": 0x008D0390,
            "Ladder's Cone": 0x008D0339,
            "Ladder's Nut": 0x008D04C4,
            "Catapult Zombie": 0x00522E8D,
            "Catapult Olive Hat": 0x008D0025,
            "Gargantuar (White Eye)": 0x00523D26,
            "Gargantuar (Red Eye)": 0x00523E4A,
            "Gargantuar's Door": 0x008D05B2,
            "Gargantuar's Bucket": 0x008D059E,
            "Gargantuar's Black Olive Hat": 0x008D0694,
            "Gargantuar's Draft Helmet": 0x008D063A,
            "Imp": 0x005227BB,
            "Plant Zombie Body": 0x005227BB,
            "Plant Zombie's Door": 0x008D01C6,
            "Plant Zombie's Cone": 0x008D01A4,
            "Plant Zombie's Bucket": 0x0052292B,
            "Wall-nut Zombie's Nut": 0x0052382B,
            "Jalapeno Zombie's Jalapeno": 0x00523A87,
            "High Ice Fruit Zombie's High Ice Fruit": 0x008D11D1,
            "Gatling Shooter Zombie": 0x008D11A2,
            "Torch Nut Zombie's Nut Head": 0x008D12EC,
            "Gatling Pole Vaulting Zombie": 0x008D1415,
            "Gatling Dolphin Zombie's Cone": 0x008D164F,
            "Disco Zombie": 0x008D0828,
            "Skeleton": 0x008D0B57,
            "Necromancer": 0x008D0D93,
            "Fire Disco Zombie": 0x008D0BF5,
            "Fire Dancer": 0x008D0D77,
            "Bed Cart": 0x008D0E58,
            "Small Fall Guy's Sleep Cap": 0x008D0EA8,
            "Rubber Ducky's Cone": 0x008D0E44,
            "Rubber Ducky's Bucket": 0x008D0E11,
            "Dr. Zomboss": 0x008D0F0B,
            "Olive Giant": 0x008D0F01,
            "Olive Giant Helmet": 0x008D0F15,
            "Olive Imp": 0x005227BB,
            "Olive Imp Helmet": 0x008D0F8C,
            "Yeti Digger Zombie": 0x008D0FC6,
            "Yeti Digger Hat": 0x008D0FA0,
            "Diamond Zombie Hat": 0x008D1DF7,
            "Shark Zombie": 0x008D1A97,
            "Siren Zombie": 0x008D1C4D,
            "Tangle Snorkel Zombie": 0x008D1CDA,
        }


plants_HP_addresses = {
    "General Plant": 0x00844DBF,
    "Torch Nut/Magnet Nut/Watermelon Nut": 0x0045E1A7,
    "Snow Ice-shroom/Burger Shooter/Shadow Squash King/Butter JOKER/Garlic Jalapeno": 0x00844DCB,
    "Pea Wishing Well": 0x00844DD7,
    "High Ice Fruit": 0x0045E215,
    "Sea Nut": 0x00850008,
    "Pea Cannon": 0x008502A6,
    "Gloom Pumpkin/Sun Pumpkin Palm/Blazing Pumpkin/Life Reshaper/Lotus Shell": 0x0045E445,
    "Charm Garlic": 0x0045E242,
    "Steel Thorn Nut King": 0x0045E5C3,
    "Doom Cannon": 0x00850296,
    "Explosion Nut": 0x0045E1BA,
    "Giant Nut": 0x0045E207,
    "Firecracker Nut Wall": 0x00850357,
    "Hot Dog Shooter": 0x00850057,
    "Sunflower Queen": 0x008500BA,
    "VIP Nut": 0x008500E6,
    "VIP Nut Grown Added HP": 0x00867E73,
    "Zombie Nut Wall": 0x00850112,
    "Cupid Charm-shroom Shooter": 0x00850130,
    "Fortune Marigold": 0x00850155,
    "Crater Nut": 0x00850165,
    "Squash Nut": 0x008501AC,
    "Squash Nut Critical HP": 0x008491AB + 3,  # Note: address needs offset added
    "Frozen Nut": 0x008501BC,
}

# plantPutType = [
#     "PeaSunflower",
#     "Sun Bean",
#     "Sun Bomb",
#     "Torch Nut",
#     "Sun Potato Mine",
#     "Ice Cattail",
#     "Garlic Flower",
#     "Double Cactus",
#     "Small Pot Mushroom",
#     "Sun Sunflower",
#     "Ice Melon Fume-shroom",
#     "Tomb Mine Layer",
#     "Red Eye Mushroom",
#     "Sun Scaredy-shroom",
#     "Snow Ice-shroom",
#     "Charm Doom-shroom",
#     "Pea Lily Pad",
#     "Ice Squash",
#     "Pea Wishing Well",
#     "Doom Seaweed",
#     "Chermander",
#     "Butter Spikeweed",
#     "Ice Torchwood",
#     "High Ice Fruit",
#     "Sea Nut",
#     "No. 6 Lamp Flower",
#     "Pea Cannon",
#     "Cactus Clover",
#     "Taco Cattail",
#     "Spikeweed Starfruit",
#     "Gloom Pumpkin",
#     "Magnet Nut",
#     "Gatling Cabbage-pult",
#     "Sun Flower Pot",
#     "Threepeater Corn",
#     "Random Plant Box",
#     "Charm Garlic",
#     "Coffee Umbrella",
#     "Cactus Clover Flower",
#     "Watermelon Nut",
#     "Burger Shooter",
#     "Sun Pumpkin Palm",
#     "Butter Gloom-shroom",
#     "Watermelon Cattail",
#     "Sun-shroom Pult",
#     "Marigold Magnet",
#     "Steel Thorn Nut King",
#     "Doom Cannon",
#     "Imitater",
#     "Explosion Nut",
#     "Giant Nut",
#     "Sprout",
#     "Firecracker Mine",
#     "Firecracker Nut Wall",
#     "Pea Cattail",
#     "Ice Melon Cattail",
#     "Blazing Pumpkin",
#     "Zombie Peashooter",
#     "Ice Clover",
#     "Hot Dog Shooter",
#     "Ice Cactus",
#     "Shadow Squash King",
#     "Butter JOKER",
#     "Sunflower Queen",
#     "Garlic Jalapeno",
#     "VIP Nut",
#     "Zombie Nut Wall",
#     "Charm-shroom Shooter",
#     "Fortune Marigold",
#     "Cat Litter Box",
#     "Crater Nut",
#     "Bouncy Fume-shroom",
#     "Ice Spikeweed",
#     "Earth Starfruit",
#     "Elf Mushroom",
#     "Sichuan Cuisine Pult",
#     "Nut Imitater",
#     "Squash Nut",
#     "Frozen Nut",
#     "Brainstorm",
#     "Treasure Devourer",
#     "Hologram Card Projector",
#     "Growth Coffee Bean",
#     "Cold Light Mushroom",
#     "Scorching Peashooter",
#     "Fluorescent Mallet",
#     "Wild Gatling Shooter",
#     "Life Reshaper",
#     "Twin Cherries",
#     "Lucky Clover",
#     "Gold Sunflower",
#     "Potato Cannon",
#     "Punishment Cage",
#     "Reserve Supplies",
#     "Spikeweed Chomper",
#     "Zombie Bean",
#     "Forbidden Doom-shroom",
#     "Match-3 Candy",
#     "Sea Ice-shroom",
#     "Lotus Shell",
#     "Kitty Sunflower",
# ]
goldPlant = [
    "High Ice Fruit",
    "Pea Cannon",
    "Gloom Pumpkin",
    "Burger Shooter",
    "Butter Gloom-shroom",
    "Watermelon Cattail",
    "Steel Thorn Nut King",
    "Doom Cannon",
    "Ice Melon Cattail",
    "Hot Dog Shooter",
    "Sunflower Queen",
    "VIP Nut",
    "Wild Gatling Shooter",
    "Ice Cannon",
    "Gold Watermelon Pult",
]
goldPlantIndex = [23, 26, 30, 40, 42, 43, 46, 47, 78, 82, 86, 88, 109]
mushroomPlant = [
    8,
    9,
    10,
    12,
    13,
    14,
    15,
    17,
    23,
    24,
    30,
    31,
    40,
    42,
    44,
    47,
    83,
    90,
    94,
    97,
    106,
    119,
    121,
]
peaPlant = [0, 16, 18, 26, 32, 40, 77, 80, 82, 107, 109]
melonPlant = [10, 39, 43, 78]
flowerPlant = [0, 2, 9, 86, 123]
bulletType = [
    "Pea",
    "Ice Pea",
    "Cabbage",
    "Watermelon",
    "Spore",
    "Ice Watermelon",
    "Fireball (Invisible)",
    "Star",
    "Cactus Needle",
    "Basketball",
    "Corn Kernel",
    "Doom-shroom",
    "Butter",
    "Zombie Pea",
    "Small Sun-shroom",
    "Large Sun-shroom",
    "Black Pea",
    "Ice Spike",
    "Charm Arrow",
    "Silver Coin",
    "Gold Coin",
    "Diamond",
    "Potato Mine",
    "Sichuan Cuisine",
    "Jalapeno",
    "White Fireball",
    "Potato Cannon (No Damage)",
    "Ice Spore",
    "Small Sun",
    "Pea Zombie's Fire Pea 1",
    "Pea Zombie's Fire Pea 2",
    "Gold Pea",
    "Large Pea",
    "Large Fire Pea",
    "Large Ice Fire Pea",
    "Ice Fire Pea",
    "Star",
    "Large Star",
    "Gold Pea 2",
    "Ice Star",
    "Gloom-shroom Pult",
    "Ice Cannon",
    "Gold Melon",
    "Fire Corn",
    "Sun Corn Cannon",  # 44
    "Red Flame Pea",  # 45
    "Purple Flame Pea",  # 46
    "Blazing Pea",  # 47
    "Large Red Flame Pea",  # 48
    "Large Purple Flame Pea",  # 49
    "Large Blazing Pea",  # 50
    "Charm-shroom (Damage)",  # 51
    "Charm-shroom (Brief Charm)",  # 52
    "Charm-shroom (Self Harm)",  # 53
    "Fried Corn Kernel",  # 54
    "Popcorn",  # 55
    "Pumpkin Cannon",  # 56
    "Explosion (Cabbage Mortar)",  # 57
    "Explosion (Corn Mortar)",  # 58
    "Vase",  # 59
    "Spikeweed",  # 60
    "Snowball",  # 61
    "Explosion (Fire Cabbage Mortar)",  # 62
    "Explosion (Fire Corn Mortar)",  # 63
    "Explosion (Fire Corn Mortar)",  # 64
    "Corn Kernel",  # 65
    "Cake",  # 66
    "Split Star",  # 67
    "Fire Star",  # 68
    "Fire Split Star",  # 69
    "Red Hot Pea",  # 70
    "Blazing Red Hot Pea",  # 71
    "Gold Pea",  # 72
    "Fire Explosion Star",  # 73
    "Explosion Star",  # 74
    "Chomper",  # 75
    "Big Chomper",  # 76
    "Green Fire Pea",  # 77
    "Steel Star",  # 78
    "Pink Star",  # 79
    "Corn Kernel",  # 80
    "Cherry Bullet",  # 81
    "Garlic Bullet",  # 82
    "Black Garlic Bullet",  # 83
    "Explosion (Cabbage Artillery)",  # 84
    "Explosion (Fire Cabbage Artillery)",  # 85
    "Money Sun",  # 86
    "Note",  # 87
    "Heavy Note",  # 88
    "Water Bullet",  # 89
    "Large Water Bullet",  # 90
    "Star (No Damage)",  # 91
    "Color Star (No Damage)",  # 92
    "Iron Cherry Bullet",  # 93
    "Gold Cherry Bullet",  # 94
    "Diamond Cherry Bullet",  # 95
    "Bandage Nut (No Damage)",  # 96
    "Fire Jalapeno Pea",  # 97
    "Banana Peel (No Damage)",  # 98
    "Scorching Cactus Needle",  # 99
    "Galaxy Star",  # 100
    "Large Galaxy Star",  # 101
    "Ice Bomb Shell",  # 102
    "Arctic Ice Melon",  # 103
    "Throwing Magnet",  # 104
    "Charge Magnet",  # 105
    "Spike Umbrella",  # 106
    "Spike",  # 107
    "Potato Spore",  # 108
    "Ice Cone",  # 109
    "Bubble",  # 110
    "Cyber Pea",  # 111
    "Cyber Fire Pea",  # 112
    "Cyber Blue Fire Pea",  # 113
    "Cyber Blazing Pea",  # 114
    "Cyber Purple Fire Pea",  # 115
    "Cyber Inferno Pea",  # 116
    "Idol Note",  # 117
    "Ice Idol Note",  # 118
    "Blazing Idol Note",  # 119
    "Purple Fire Idol Note",  # 120
    "Inferno Idol Note",  # 121
    "Gold Pea 3",  # 122
    "Fire Gold Pea",  # 123
    "Ice Fire Gold Pea",  # 124
    "Sun Fireball",  # 125
    "Cactus Point Defense Cannon",  # 126
    "Sun Shooter Bullet",  # 127
]
keyTpye = [
    "None",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "Numpad 0",
    "Numpad 1",
    "Numpad 2",
    "Numpad 3",
    "Numpad 4",
    "Numpad 5",
    "Numpad 6",
    "Numpad 7",
    "Numpad 8",
    "Numpad 9",
    "Numpad *",
    "Numpad +",
    "Numpad -",
    "Numpad .",
    "Numpad /",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
    "~",
]

keyCode = [
    "",
    0x30,
    0x31,
    0x32,
    0x33,
    0x34,
    0x35,
    0x36,
    0x37,
    0x38,
    0x39,
    0x41,
    0x42,
    0x43,
    0x44,
    0x45,
    0x46,
    0x47,
    0x48,
    0x49,
    0x4A,
    0x4B,
    0x4C,
    0x4D,
    0x4E,
    0x4F,
    0x50,
    0x51,
    0x52,
    0x53,
    0x54,
    0x55,
    0x56,
    0x57,
    0x58,
    0x59,
    0x5A,
    0x60,
    0x61,
    0x62,
    0x63,
    0x64,
    0x65,
    0x66,
    0x67,
    0x68,
    0x69,
    0x6A,
    0x6B,
    0x6D,
    0x6E,
    0x6F,
    0x70,
    0x71,
    0x72,
    0x73,
    0x74,
    0x75,
    0x76,
    0x77,
    0x78,
    0x79,
    0x7A,
    0x7B,
    0xC0,
]

TREE_OF_WISDOM_REWARD = [
    (10, "Tree of Wisdom gives you 10 packs of fertilizer"),
    (20, "Tree of Wisdom gives you 20 chocolates"),
    (30, "Tree of Wisdom gives you a Sprinkler Pool Cleaner"),
    (50, "Tree of Wisdom gives you a Fertilizer Wheelbarrow"),
    (100, "Tree of Wisdom gives you a Card Shovel"),
    (150, "Tree of Wisdom gives you a Gold Sprinkler Pool Cleaner"),
    (200, "Tree of Wisdom gives you a Music Roof Cleaner"),
    (300, "Tree of Wisdom gives you [Dream Color Card] Glove Bean"),
    (400, "Tree of Wisdom gives you a new garden scene [Cozy Garden]"),
    (500, "Tree of Wisdom gives you [Dream Color Card] Cornucopia"),
    (600, "Tree of Wisdom gives you a new garden scene [Charm Mushroom Garden]"),
    (700, "Tree of Wisdom gives you [Dream Color Card] Watering Can Pult"),
    (800, "Tree of Wisdom gives you a new garden scene [Arena Garden]"),
    (900, "Tree of Wisdom unlocks the glove function. Press 'GGG' to use the glove, costing 10 gold each time"),
    (1000, "Tree of Wisdom gives you a Wisdom Shovel"),
    (1100, "Tree of Wisdom gives you 100 packs of fertilizer"),
    (1200, "Tree of Wisdom gives you 200 chocolates"),
    (1300, "Tree of Wisdom gives you 300 pesticides"),
    (1500, "Tree of Wisdom gives you a Gold Medal Snail [can fertilize + water + collect money for plants]"),
    (2025, "Tree of Wisdom gives you a 2025 Gramophone [satisfies the musical needs of all plants]"),
]
TREE_OF_WISDOM = [
    (1, "Thank you for nurturing me! As long as you keep giving me fertilizer, I will give you valuable information and items!"),
    (
        2,
        "When your nuts are injured, you can directly cover them with the same type of nut. This is called 'Nut Bandaging Technique'.",
    ),
    (3, "If you need to replace the flower pot under a plant, just plant a new pot directly on top of it."),
    (4, "Just like Lotus Shell is a pumpkin shell, Flower Pot Lily Pad is essentially a Lily Pad — so it doesn't respond to pot replacement."),
    (
        5,
        "The Gardener Zombie's trolley is amazing. Sometimes it turns exploding plants back into cards. What bug? This is a feature!",
    ),
    (6, "You may have noticed that zombies sometimes drop a picture album. They are all collected to the left of the first chapter album."),
    (
        7,
        "The stinky snail in the garden can help you water, but his eyesight doesn't seem too good... or maybe he's just not used to this job yet, I guess.",
    ),
    (
        8,
        "Some mushroom hybrid plants still sleep during the day. I think it's because they have more mushroom genes. You can check the Almanac to find out who these sleepyheads are.",
    ),
    (9, "Hey, I'm 10 meters tall! Please accept these 10 packs of fertilizer as a small gift of my gratitude!"),
    (10, "It's said that the deep pit on the achievement screen goes straight to the other side of the earth. Want to quickly return to the top? Try pressing Esc."),
    (11, "Open your eyes wide and look carefully next to your seed selection interface... that small 'Introduction' lets you check plant characteristics anytime."),
    (12, "I heard that pressing '6' during a level can jump to the shop. But what is '6'? Do you have any idea?"),
    (13, "Rich Man Zombie has endless coins to throw, but money-type plants aren't afraid of it, especially Nut Piggy Bank."),
    (
        14,
        "High Ice Fruit Zombie's head has 8000 HP, very durable. But it won't tell you that's actually a mask — its body isn't that strong.",
    ),
    (
        15,
        "Freeze and slow effects are 'cool', but not so cool when they land on plants... fortunately, ice and fire type plants aren't affected.",
    ),
    (
        16,
        "Apple Alarm Clock is a time stopper, but it also has a regular alarm function. You can use it to wake up sleeping things, including plants... and certain zombies?",
    ),
    (17, "Frost Giant's ice ball isn't that tough. Enough firepower, or a bomb, can shatter it."),
    (
        18,
        "Torch Jalapeno's flames can protect nearby plants from ice effects. Maybe it could also be used for next Saturday's marshmallow roast?",
    ),
    (19, "Wow! I'm 20 meters tall! Take these chocolates, let's celebrate with some sweets!"),
    (
        20,
        "Disco Zombie is strong, but when he tries to fly over the defense line with balloons, he gets easily taken down by clover or bombs... there are no shortcuts in this world.",
    ),
    (
        21,
        "Blast Door Zombie's shield has unimaginable blast resistance. But just as even the most perfect things have their flaws, this door can't stop bubbles.",
    ),
    (
        22,
        "Edgar Jr.'s fireballs look unstoppable, but don't worry! Most healthy nuts can block one fireball — they're reliable.",
    ),
    (
        23,
        "I heard the zombie bugs underground are hiding some secret. Want to catch one and see? Come share your discoveries with me.",
    ),
    (
        24,
        "Cactus Clover Flower's wind isn't as strong as other clovers, but it can still blow away fog. After all, fog is lighter than zombies, isn't it?",
    ),
    (
        25,
        "Crater Nut claims there's a 4D fragment on top of his head, and if he's not careful, he might turn into a black hole... do you believe that?",
    ),
    (
        26,
        "When you defeat a boss zombie, it might drop a large diamond cluster worth 100 diamonds!",
    ),
    (
        27,
        "Thunder Fruit seems to be hybridized from two plants from outside this world. He says his birth depends on some long-standing whimsical ideas.",
    ),
    (
        28,
        "Melon Fume-shroom told me he's been feeling down lately: people still think Watermelon Fume-shroom replaced him. How does he prove he's still here...",
    ),
    (29, "Wow, I'm already 30 meters tall! This sprinkler pool cleaner is my thank-you gift, hope it can help you!"),
    (
        30,
        "Magnetic Field Zombie's magnetic source is actually the glowing core on its back. That's why it doesn't need a helmet to attract fire.",
    ),
    (
        31,
        "Charm-shroom Shooter and Psychedelic Pult look like twin sisters, but they're actually distant relatives... though they were once roommates.",
    ),
    (32, "Card Imitater and Imitater are not the same plant. As for where Imitater is? You can find him in the usual place."),
    (
        33,
        "Have you heard? Baptized Threepeater comes from another world. Burger Shooter said he once traveled there and saw many novel things.",
    ),
    (
        34,
        "Is there a popular song recently? Card Imitater often wears headphones and loops it. I can vaguely hear something like 'Wood hut buy buy buy'...",
    ),
    (
        35,
        "It's said that the history of hybrid plants is much older than Dave's experiments. Some plants were born long before PeaSunflower... this is a secret story.",
    ),
    (
        36,
        "Prism Sunflower told me she couldn't tell glass from diamonds when she was little... so she always thought she was Diamond Sunflower back then.",
    ),
    (
        37,
        "Legend has it that this world underwent an earth-shattering change after the hero descended... As for the truth of this legend, maybe you know better than I do?",
    ),
    (38, "Cat Star Gatling came to chat with me recently, asking why some Gatlings here like to wear capes..."),
    (
        39,
        "Those blue ice fireballs, I remember their color used to be deeper. Maybe Ice Torchwood supplemented some trace elements later.",
    ),
    (
        40,
        "Does the decoration on the front of Balloon Cart Zombie look familiar? That guy really likes the clown decoration from his Jack-in-the-Box, so he customized a larger one.",
    ),
    (
        41,
        "It's said that High Ice Fruit became famous in a random plant battle. Everyone who watched that video started calling him 'God of War'.",
    ),
    (42, "You ask what Bouncy Fume-shroom's 'one day' means?... Trust me, you don't want to know."),
    (
        43,
        "Did you know? The seemingly lazy Cat Bed actually exercises every day to lose fat. It used to be much fatter than now.",
    ),
    (
        44,
        "Recycle Tall-nut says he spends time every day changing the shovel decoration layout on his head, but in the end, he feels cat ears suit him best.",
    ),
    (
        45,
        "It's said Sunflower Princess has had plastic surgery, but I know that's just gossip. Actually, she just accidentally booked a ticket to Africa... and got tanned.",
    ),
    (
        46,
        "Gold Watermelon Pult, Gold Sunflower, Evolution Bean, Golden Sunflower — these four plants are distant relatives... their prototypes were all trophies.",
    ),
    (
        47,
        "There are rumors that cattail-type plants have 'magic'... I don't know where that came from, but their tracking ability really is like magic.",
    ),
    (
        48,
        "I'll tell you secretly: Burger Shooter sometimes complains to me that his hair is too thick and covers his eyes. But I've never seen him actually get a haircut.",
    ),
    (
        49,
        "Wow, I've grown to 50 meters! Do you need more functional tools? This fertilizer wheelbarrow might suit you!",
    ),
    (100, "Wow, I'm 100 meters tall! Thank you for nurturing me, please accept this Card Shovel!"),
    (150, "Aha! I'm already 150 meters! It's time to upgrade your sprinkler pool cleaner to a gold-plated version!"),
    (
        200,
        "Oh, I've actually grown to 200 meters! This music roof cleaner is my thank-you gift, you can use it to defend the roof!",
    ),
    (
        300,
        "Thank you for raising me to 300 meters! This Glove Bean will stick with you from now on. I believe it can help you!",
    ),
    (400, "Gosh, I'm 400 meters tall! In return, this Cozy Garden will be open to you from now on!"),
    (500, "Unbelievable, I've reached 500 meters! This Cornucopia can produce coins for you. I think you'll need it!"),
    (
        600,
        "Awesome, I'm 600 meters tall! Here's the key to the Charm Mushroom Garden. Now you have more space to grow mushrooms!",
    ),
    (
        700,
        "I never thought I could grow to 700 meters! I brought you a new plant. Hope this Watering Can Pult becomes your ally!",
    ),
    (
        800,
        "Yo, I'm 800 meters tall! This Arena Garden is prepared for you. Now you have more space for your potted plants!",
    ),
    (
        900,
        "Wow, I'm 900 meters tall! Press the 'G' key three times in a row during a level to spend 10 gold coins to use the glove!",
    ),
    (1000, "Finally! I've reached the 1000 meter milestone! Let this Wisdom Shovel represent my gratitude to you!"),
    (
        1100,
        "Ha, I've grown to 1100 meters! Time to treat! Use these 100 packs of fertilizer to feed the plants in your garden!",
    ),
    (
        1200,
        "I've grown to 1200 meters! Maybe 200 chocolates aren't enough to fully express my gratitude. I'll bring better gifts later!",
    ),
    (1300, "The view at 1300 meters is awesome! These 300 pesticides are my recent stock, feel free to take them!"),
    (
        1400,
        "Unbelievable! I'm 1500 meters tall! This gold medal snail is a garden management expert, it can help you fertilize plants!",
    ),
    (
        2025,
        "Yahoo! 2025 meters, a commemorative height! Use this 2025 gramophone that echoes through the venue to make your garden rock out with music!",
    ),
    (2026, "Thank you for your care! I've given you all my wisdom, but you can still make me grow taller!"),
    (
        40000,
        "Thank you for fertilizing me! I'm a bit short on new wisdom now. But if you plant me higher, I'll prepare more gifts for you!",
    ),
    (40001, "When you live as long as I have, you'll sleep less and hallucinate more easily."),
    (
        40002,
        "If you can't figure out what is a forest and what is a tree, just remember: a forest is a collection of individual trees, but not the other way around.",
    ),
    (40003, "History keeps repeating itself, but certain details are always different."),
    (
        40004,
        "If the past, present, and future exist simultaneously as a trinity forming a 'cycle', then the experiential 'present' might be nothing more than an elaborate illusion?",
    ),
    (40005, "Courage is easy to come by, dedication is hard to find."),
    (40006, "I have some time-tested wisdom..."),
    (40007, "Please give me some fertilizer!"),
    (40008, "I'm really, really grateful for your spending on fertilizer for me!"),
    (40009, "That cloud looks just like a big water droplet!"),
    (40010, "Have you seen my cousin Yggdrasil? Very big! Lives in Sweden, has lots of fans."),
    (40011, "I'm studying sociology at an online university. I've really learned a lot."),
    (
        40012,
        "After careful observation, I've deduced that the Earth revolves around the Sun, not the other way around as we see.",
    ),
    (40013, "Mmm... sunlight is delicious!"),
    (40014, "Oh, sorry... I just released some oxygen."),
    (40015, "Oh my, I'm growing leaves!"),
    (40016, "I feel like I'm going to burst!"),
    (40017, "I'm currently lacking some knowledge about worldviews!"),
    (40018, "Mmm, I'm sure I enjoyed some delicious fertilizer!"),
    (40019, "I think I've seen clouds before."),
    (40020, "I'll just keep growing tall here."),
    (40021, "I'm metabolizing!"),
    (40022, "I don't really understand how you animals can walk around all day long..."),
    (40023, "Time is very slow for me!"),
    (40024, "I think I'm perennial!"),
    (40025, "My xylem is tingling!"),
    (40026, "Just standing by my side, you can gain lots and lots of wisdom."),
    (40027, "I've heard of 'winter'. But I'm not looking forward to that kind of day."),
    (
        40028,
        "Hey, I'm 100 feet tall! Celebrate! Type 'daisies' to make zombies leave a little daisy when they die.",
    ),
    (40029, "Aha! I'm 500 feet tall! Let's dance! Type 'dance' to make all the zombies boogie!"),
    (
        40030,
        "Whoa! I'm 1000 feet tall! Type 'pinata' with me to make zombies spit out candy when they die. Let's celebrate!",
    ),
]


class plant:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0x148)
        self.exist = PVZ_memory.read_bool(self.addr + 0x141)
        self.x = PVZ_memory.read_uint(self.addr + 0x8)
        self.y = PVZ_memory.read_uint(self.addr + 0xC)
        self.row = PVZ_memory.read_uint(self.addr + 0x1C)
        self.col = PVZ_memory.read_uint(self.addr + 0x28)
        self.type = PVZ_memory.read_uint(self.addr + 0x24)
        # 2c shake countdown
        # 30 shake animation index
        self.state = PVZ_memory.read_uint(self.addr + 0x3C)
        self.hp = PVZ_memory.read_uint(self.addr + 0x40)  # HP
        self.maxhp = PVZ_memory.read_uint(self.addr + 0x44)
        self.dieTime = PVZ_memory.read_uint(self.addr + 0x4C)
        self.cinderTime = PVZ_memory.read_uint(self.addr + 0x50)
        self.effectTime = PVZ_memory.read_uint(self.addr + 0x54)  # Sun Bean growth
        self.productTime = PVZ_memory.read_uint(self.addr + 0x58)  # Normal attack
        self.productInterval = PVZ_memory.read_uint(self.addr + 0x5C)  # Normal attack interval
        self.attackTime = PVZ_memory.read_uint(self.addr + 0x90)
        self.sunTime = PVZ_memory.read_uint(self.addr + 0xDC)
        self.humTime = PVZ_memory.read_uint(self.addr + 0x128)  # Sun production
        self.mushroomTime = PVZ_memory.read_uint(self.addr + 0x130)
        self.isVisible = PVZ_memory.read_bool(self.addr + 0x18)
        self.isSquash = PVZ_memory.read_bool(self.addr + 0x142)
        self.isSleep = PVZ_memory.read_bool(self.addr + 0x143)
        self.isLight = PVZ_memory.read_bool(self.addr + 0x145)
        self.isAttack = PVZ_memory.read_uint(self.addr + 0x48)

    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr + 0x141, exist)

    def setX(self, x):
        PVZ_memory.write_int(self.addr + 0x8, x)

    def setY(self, y):
        PVZ_memory.write_int(self.addr + 0xC, y)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr + 0x1C, row)

    def setCol(self, col):
        PVZ_memory.write_int(self.addr + 0x28, col)

    def setType(self, type):
        PVZ_memory.write_int(self.addr + 0x24, type)

    def setState(self, state):
        PVZ_memory.write_int(self.addr + 0x3C, state)

    def setHP(self, hp):
        PVZ_memory.write_int(self.addr + 0x40, hp)
        PVZ_memory.write_int(self.addr + 0x44, hp)

    def setDieTime(self, dieTime):
        PVZ_memory.write_int(self.addr + 0x4C, dieTime)

    def setCinderTime(self, cinderTime):
        PVZ_memory.write_int(self.addr + 0x50, cinderTime)

    def setEffectTime(self, effectTime):
        PVZ_memory.write_int(self.addr + 0x54, effectTime)

    def setProductTime(self, productTime):
        PVZ_memory.write_int(self.addr + 0x58, productTime)

    def setAttackTime(self, attackTime):
        PVZ_memory.write_int(self.addr + 0x90, attackTime)

    def setProductInterval(self, productInterval):
        PVZ_memory.write_int(self.addr + 0x5C, productInterval)

    def setSunTime(self, sunTime):
        PVZ_memory.write_int(self.addr + 0xDC, sunTime)

    def setHumTime(self, humTime):
        PVZ_memory.write_int(self.addr + 0x12C, humTime)

    def setmushroomTime(self, mushroomTime):
        PVZ_memory.write_int(self.addr + 0x130, mushroomTime)

    def setIsVisible(self, isVisible):
        PVZ_memory.write_bool(self.addr + 0x18, isVisible)

    def setIsSquash(self, isSquash):
        PVZ_memory.write_bool(self.addr + 0x142, isSquash)

    def setIsSleep(self, isSleep):
        PVZ_memory.write_bool(self.addr + 0x143, isSleep)

    def setIsLight(self, isLight):
        PVZ_memory.write_bool(self.addr + 0x145, isLight)

    def setIsAttack(self, isAttack):
        PVZ_memory.write_int(self.addr + 0x48, isAttack)


class zombie:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0x158)
        self.exist = PVZ_memory.read_uint(self.addr + 0xEC)
        self.row = PVZ_memory.read_uint(self.addr + 0x1C) + 1
        self.type = PVZ_memory.read_uint(self.addr + 0x24)
        self.x = PVZ_memory.read_float(self.addr + 0x2C)
        self.y = PVZ_memory.read_float(self.addr + 0x30)
        self.size = PVZ_memory.read_float(self.addr + 0x11C)
        self.state = PVZ_memory.read_uint(self.addr + 0x28)
        self.hp = PVZ_memory.read_uint(self.addr + 0xC8)
        self.maxHP = PVZ_memory.read_uint(self.addr + 0xCC)
        self.hatType = PVZ_memory.read_uint(self.addr + 0xC4)
        self.hatHP = PVZ_memory.read_uint(self.addr + 0xD0)
        self.maxHatHP = PVZ_memory.read_uint(self.addr + 0xD4)
        self.doorType = PVZ_memory.read_uint(self.addr + 0xD8)
        self.doorHP = PVZ_memory.read_uint(self.addr + 0xDC)
        self.maxDoorHP = PVZ_memory.read_uint(self.addr + 0xE0)
        self.slow = PVZ_memory.read_uint(self.addr + 0xAC)
        self.butter = PVZ_memory.read_uint(self.addr + 0xB0)
        self.frozen = PVZ_memory.read_uint(self.addr + 0xB4)
        self.isVisible = PVZ_memory.read_bool(self.addr + 0x18)
        self.isEating = PVZ_memory.read_bool(self.addr + 0x51)
        self.isHpynotized = PVZ_memory.read_bool(self.addr + 0xB8)
        self.isBlow = PVZ_memory.read_bool(self.addr + 0xB9)
        self.isDying = PVZ_memory.read_bool(self.addr + 0xBA)
        self.isGarlic = PVZ_memory.read_bool(self.addr + 0xBF)
        self.stolenPlant = PVZ_memory.read_ushort(self.addr + 0x128)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr + 0x1C, row - 1)

    def setX(self, x):
        PVZ_memory.write_float(self.addr + 0x2C, x)

    def setY(self, y):
        PVZ_memory.write_float(self.addr + 0x30, y)

    def setSize(self, size):
        PVZ_memory.write_float(self.addr + 0x11C, size)

    def setState(self, state):
        PVZ_memory.write_int(self.addr + 0x28, state)

    def setHP(self, hp):
        PVZ_memory.write_int(self.addr + 0xC8, hp)
        PVZ_memory.write_int(self.addr + 0xCC, hp)

    def setHatHP(self, hatHP):
        PVZ_memory.write_int(self.addr + 0xD0, hatHP)
        PVZ_memory.write_int(self.addr + 0xD4, hatHP)

    def setDoorHP(self, doorHP):
        PVZ_memory.write_int(self.addr + 0xDC, doorHP)
        PVZ_memory.write_int(self.addr + 0xE0, doorHP)

    def setSlow(self, slow):
        PVZ_memory.write_int(self.addr + 0xAC, slow)

    def setButter(self, butter):
        PVZ_memory.write_int(self.addr + 0xB0, butter)

    def setFrozen(self, frozen):
        PVZ_memory.write_int(self.addr + 0xB4, frozen)

    def setExist(self, exist):
        PVZ_memory.write_int(self.addr + 0xEC, exist)

    def setIsVisible(self, isVisible):
        PVZ_memory.write_bool(self.addr + 0x18, isVisible)

    def setIsEating(self, isEating):
        PVZ_memory.write_bool(self.addr + 0x51, isEating)

    def setIsHPynotized(self, isHPynotized):
        PVZ_memory.write_bool(self.addr + 0xB8, isHPynotized)

    def setIsBlow(self, isBlow):
        PVZ_memory.write_bool(self.addr + 0xB9, isBlow)

    def setIsDying(self, isDying):
        PVZ_memory.write_bool(self.addr + 0xBA, isDying)

    def setIsGarlic(self, isGarlic):
        PVZ_memory.write_bool(self.addr + 0xBF, isGarlic)

    def setStolenPlant(self, stolenPlant):
        PVZ_memory.write_ushort(self.addr + 0x128, stolenPlant)


class item:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0xE8)
        self.exist = PVZ_memory.read_bool(self.addr + 0x20)
        self.row = PVZ_memory.read_uint(self.addr + 0x14) + 1
        self.col = PVZ_memory.read_uint(self.addr + 0x10) + 1
        self.type = PVZ_memory.read_uint(self.addr + 0x8)
        self.time = PVZ_memory.read_uint(self.addr + 0x18)
        self.vase_skin = PVZ_memory.read_uint(self.addr + 0xC)
        self.vase_zombie = PVZ_memory.read_uint(self.addr + 0x3C)
        self.vase_plant = PVZ_memory.read_uint(self.addr + 0x40)
        self.vase_type = PVZ_memory.read_uint(self.addr + 0x44)
        self.vase_sun = PVZ_memory.read_uint(self.addr + 0x50)
        self.vase_see_time = PVZ_memory.read_uint(self.addr + 0x4C)

    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr + 0x20, exist)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr + 0x14, row - 1)

    def setCol(self, col):
        PVZ_memory.write_int(self.addr + 0x10, col - 1)

    def setTime(self, time):
        PVZ_memory.write_int(self.addr + 0x18, time)

    def setVaseSkin(self, vase_skin):
        PVZ_memory.write_int(self.addr + 0xC, vase_skin)

    def setVaseZombie(self, vase_zombie):
        PVZ_memory.write_int(self.addr + 0x3C, vase_zombie)

    def setVasePlant(self, vase_plant):
        PVZ_memory.write_int(self.addr + 0x40, vase_plant)

    def setVaseType(self, vase_type):
        PVZ_memory.write_int(self.addr + 0x44, vase_type)

    def setVaseSun(self, vase_sun):
        PVZ_memory.write_int(self.addr + 0x50, vase_sun)

    def setVaseSeeTime(self, vase_see_time):
        PVZ_memory.write_int(self.addr + 0x4C, vase_see_time)


class car:
    def __init__(self, addr):
        self.addr = addr
        self.exist = PVZ_memory.read_bool(self.addr + 0x30)
        self.no = PVZ_memory.read_ushort(self.addr + 0x44)
        self.row = PVZ_memory.read_uint(self.addr + 0x14)

    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr + 0x30, exist)


class slot:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0x2C)
        self.canUse = PVZ_memory.read_bool(self.addr + 0x48)
        self.type = PVZ_memory.read_uint(self.addr + 0x34)
        self.imitaterType = PVZ_memory.read_uint(self.addr + 0x34)
        self.cooldown = PVZ_memory.read_uint(self.addr + 0x28)
        self.elapsed = PVZ_memory.read_uint(self.addr + 0x24)
        self.isVisible = PVZ_memory.read_bool(self.addr + 0x18)
        self.count = PVZ_memory.read_uint(self.addr + 0x4C)

    def setCanUse(self, canUse):
        PVZ_memory.write_bool(self.addr + 0x48, canUse)

    def setType(self, type):
        PVZ_memory.write_int(self.addr + 0x34, type)

    def setImitaterType(self, imitaterType):
        PVZ_memory.write_int(self.addr + 0x34, imitaterType)

    def setCooldown(self, cooldown):
        PVZ_memory.write_int(self.addr + 0x28, cooldown)

    def setElapsed(self, elapsed):
        PVZ_memory.write_int(self.addr + 0x24, elapsed)

    def setIsVisible(self, isVisible):
        PVZ_memory.write_bool(self.addr + 0x18, isVisible)

    def setCount(self, count):
        PVZ_memory.write_int(self.addr + 0x4C, count)


class plantCharacteristic:
    def __init__(self, type):
        self.type = type
        if PVZ_version == 3.16 or PVZ_version == 3.17:
            if type < 512:
                self.addr = 0x00EF4010 + type * 0x24
                self.sun = PVZ_memory.read_uint(self.addr)
                self.cd = PVZ_memory.read_uint(self.addr + 0x4)
                self.canAttack = PVZ_memory.read_bool(self.addr + 0x8)
                self.attackInterval = PVZ_memory.read_uint(self.addr + 0xC)
            else:
                self.addr = 0x0088B1A9 + (type - 512) * 0x4
                self.sun = PVZ_memory.read_uint(self.addr)
                self.cd = 0
                self.canAttack = True
                self.attackInterval = 0

        elif (
            isinstance(PVZ_version, (int, float))
            and PVZ_version < 3.4
            and PVZ_version != 3.11
            and PVZ_version != 3.12
            and PVZ_version != 3.132
            and PVZ_version != 3.14
            and PVZ_version != 3.151
        ):
            if type < 256:
                self.addr = 0x007A2010 + type * 0x24
                self.sun = PVZ_memory.read_uint(self.addr)
                self.cd = PVZ_memory.read_uint(self.addr + 0x4)
                self.canAttack = PVZ_memory.read_bool(self.addr + 0x8)
                self.attackInterval = PVZ_memory.read_uint(self.addr + 0xC)
            else:
                if PVZ_version == 2.0:
                    self.addr = 0x008452C8 + type - 256
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.addr = 0x0088B018 + type - 256
                    self.sun = PVZ_memory.read_uchar(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 2.3:
                    self.addr = 0x00088B04D + (type - 256) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 2.35 or PVZ_version == 2.36 or PVZ_version == 2.37:
                    self.addr = 0x0088B05D + (type - 256) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 2.4 or PVZ_version == 2.5 or PVZ_version == 2.51:
                    self.addr = 0x0088B072 + (type - 256) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 2.6 or PVZ_version == 2.61:
                    self.addr = 0x0088B072 + (type - 256) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 3.0:
                    self.addr = 0x0088B0F9 + (type - 256) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 3.1 or PVZ_version == 3.15:
                    self.addr = 0x0088B0F9 + (type - 256) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 3.2 or PVZ_version == 3.21 or PVZ_version == 3.3:
                    self.addr = 0x0088B119 + (type - 256) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
        else:
            if type < 512:
                self.addr = 0x007A2010 + type * 0x24
                self.sun = PVZ_memory.read_uint(self.addr)
                self.cd = PVZ_memory.read_uint(self.addr + 0x4)
                self.canAttack = PVZ_memory.read_bool(self.addr + 0x8)
                self.attackInterval = PVZ_memory.read_uint(self.addr + 0xC)
            else:
                if PVZ_version == 3.4:
                    self.addr = 0x0088B119 + (type - 512) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                if PVZ_version == 3.5 or PVZ_version == 3.6:
                    self.addr = 0x0088B129 + (type - 512) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                if PVZ_version == 3.65:
                    self.addr = 0x0088B14A + (type - 512) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                if PVZ_version == 3.7 or PVZ_version == 3.75 or PVZ_version == 3.76:
                    self.addr = 0x0088B16B + (type - 512) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                if PVZ_version == 3.8 or PVZ_version == 3.9:
                    self.addr = 0x0088B16B + (type - 512) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif PVZ_version == 3.99:
                    self.addr = 0x0088B184 + (type - 512) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0
                elif (
                    PVZ_version == 3.11
                    or PVZ_version == 3.12
                    or PVZ_version == 3.132
                    or PVZ_version == 3.14
                    and PVZ_version == 3.151
                ):
                    self.addr = 0x0088B1A9 + (type - 512) * 0x4
                    self.sun = PVZ_memory.read_uint(self.addr)
                    self.cd = 0
                    self.canAttack = True
                    self.attackInterval = 0

    def setSun(self, sun):
        PVZ_memory.write_int(self.addr, sun)

    def setCd(self, cd):
        PVZ_memory.write_int(self.addr + 0x4, cd)

    def setCanAttack(self, canAttack):
        PVZ_memory.write_bool(self.addr + 0x8, canAttack)

    def setAttackInterval(self, attackInterval):
        PVZ_memory.write_int(self.addr + 0xC, attackInterval)


class zombieType:
    def __init__(self, type):
        self.type = type
        if PVZ_version < 2.3:
            if type <= 54:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 51:
                if PVZ_version == 2.0:
                    self.weight = PVZ_memory.read_uchar(0x0085A887)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.weight = PVZ_memory.read_uchar(0x008D0887)
            elif type == 52:
                if PVZ_version == 2.0:
                    self.weight = PVZ_memory.read_uchar(0x0085A75F)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.weight = PVZ_memory.read_uchar(0x008D075F)
            elif type == 53:
                if PVZ_version == 2.0:
                    self.weight = PVZ_memory.read_uchar(0x0085A538)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.weight = PVZ_memory.read_uchar(0x008D0538)
            elif type == 54:
                if PVZ_version == 2.0:
                    self.weight = PVZ_memory.read_uchar(0x0085A613)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.weight = PVZ_memory.read_uchar(0x008D0613)
        elif PVZ_version == 2.3:
            if type <= 55:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 56:
                self.weight = PVZ_memory.read_uchar(0x008D0882)
            elif type == 57:
                self.weight = PVZ_memory.read_uchar(0x008D0743)
            elif type == 58:
                self.weight = PVZ_memory.read_uchar(0x008D051C)
            elif type == 59:
                self.weight = PVZ_memory.read_uchar(0x008D05F7)
        elif PVZ_version == 2.35 or PVZ_version == 2.36 or PVZ_version == 2.37:
            if type <= 58:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 59:
                self.weight = PVZ_memory.read_uchar(0x008D0896)
            elif type == 60:
                self.weight = PVZ_memory.read_uchar(0x008D0743)
            elif type == 61:
                self.weight = PVZ_memory.read_uchar(0x008D051C)
            elif type == 62:
                self.weight = PVZ_memory.read_uchar(0x008D05F7)
        elif PVZ_version == 2.4:
            if type <= 63:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 64:
                self.weight = PVZ_memory.read_uchar(0x008D0896)
            elif type == 65:
                self.weight = PVZ_memory.read_uchar(0x008D0743)
            elif type == 66:
                self.weight = PVZ_memory.read_uchar(0x008D051C)
            elif type == 67:
                self.weight = PVZ_memory.read_uchar(0x008D05F7)
        elif PVZ_version == 2.5 or PVZ_version == 2.51:
            if type <= 65:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 66:
                self.weight = PVZ_memory.read_uchar(0x008D0896)
            elif type == 67:
                self.weight = PVZ_memory.read_uchar(0x008D0743)
            elif type == 68:
                self.weight = PVZ_memory.read_uchar(0x008D051C)
            elif type == 69:
                self.weight = PVZ_memory.read_uchar(0x008D05F7)
        elif PVZ_version == 2.6:
            if type <= 74:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 75:
                self.weight = PVZ_memory.read_uchar(0x008D08C7)
            elif type == 76:
                self.weight = PVZ_memory.read_uchar(0x008D0774)
            elif type == 77:
                self.weight = PVZ_memory.read_uchar(0x008D0528)
            elif type == 78:
                self.weight = PVZ_memory.read_uchar(0x008D061B)
        elif PVZ_version == 2.61:
            if type <= 75:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 76:
                self.weight = PVZ_memory.read_uchar(0x008D08C7)
            elif type == 77:
                self.weight = PVZ_memory.read_uchar(0x008D0774)
            elif type == 78:
                self.weight = PVZ_memory.read_uchar(0x008D0528)
            elif type == 79:
                self.weight = PVZ_memory.read_uchar(0x008D061B)
        elif PVZ_version == 3.0:
            if type <= 83:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 84:
                self.weight = PVZ_memory.read_uchar(0x008D08C7)
            elif type == 85:
                self.weight = PVZ_memory.read_uchar(0x008D0774)
            elif type == 86:
                self.weight = PVZ_memory.read_uchar(0x008D0528)
            elif type == 87:
                self.weight = PVZ_memory.read_uchar(0x008D061B)
        elif (
            PVZ_version == 3.1
            or PVZ_version == 3.15
            or PVZ_version == 3.2
            or PVZ_version == 3.21
        ):
            if type <= 89:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 90:
                self.weight = PVZ_memory.read_uchar(0x008D0927)
            elif type == 91:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 92:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 93:
                self.weight = PVZ_memory.read_uchar(0x008D066B)

        elif PVZ_version == 3.3 or PVZ_version == 3.4:
            if type <= 95:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 96:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 97:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 98:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 99:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.5:
            if type <= 101:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 102:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 103:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 104:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 105:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.6:
            if type <= 103:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 104:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 105:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 106:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 107:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.65:
            if type <= 106:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 107:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 108:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 109:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 110:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.7 or PVZ_version == 3.75 or PVZ_version == 3.76:
            if type <= 109:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 110:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 111:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 112:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 113:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.8:
            if type <= 111:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 112:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 113:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 114:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 115:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.9:
            if type <= 114:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 115:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 116:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 117:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 118:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.99 or PVZ_version == 3.11 or PVZ_version == 3.12:
            if type <= 114:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 115:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 116:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 117:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 118:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.132:
            if type <= 117:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 118:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 119:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 120:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 121:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.14:
            if type <= 125:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 126:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 127:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 128:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 129:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.151:
            if type <= 130:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 131:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 132:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 133:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 134:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.16:
            if type <= 131:
                self.addr = 0x007A8000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 132:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 133:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 134:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 135:
                self.weight = PVZ_memory.read_uchar(0x008D066B)
        elif PVZ_version == 3.17:
            if type <= 138:
                self.addr = 0x007A8000 + type * 0x1C
                self.anime = PVZ_memory.read_uint(self.addr + 0x4)
                self.level = PVZ_memory.read_uint(self.addr + 0x8)
                self.weight = PVZ_memory.read_uint(self.addr + 0x14)
            elif type == 139:
                self.weight = PVZ_memory.read_uchar(0x008D0928)
            elif type == 140:
                self.weight = PVZ_memory.read_uchar(0x008D07C4)
            elif type == 141:
                self.weight = PVZ_memory.read_uchar(0x008D0529)
            elif type == 142:
                self.weight = PVZ_memory.read_uchar(0x008D066B)

    def setAnime(self, anime):
        PVZ_memory.write_int(self.addr + 0x4, anime)

    def setLevel(self, level):
        PVZ_memory.write_int(self.addr + 0x4, level)

    def setWeight(self, weight):
        if PVZ_version < 2.3:
            if self.type <= 50:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 51:
                if PVZ_version == 2.0:
                    PVZ_memory.write_uchar(0x0085A887, weight)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    PVZ_memory.write_uchar(0x008D089E, weight)
            elif self.type == 52:
                if PVZ_version == 2.0:
                    PVZ_memory.write_uchar(0x0085A75F, weight)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    PVZ_memory.write_uchar(0x008D075F, weight)
            elif self.type == 53:
                if PVZ_version == 2.0:
                    PVZ_memory.write_uchar(0x0085A538, weight)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    PVZ_memory.write_uchar(0x008D0538, weight)
            elif self.type == 54:
                if PVZ_version == 2.0:
                    PVZ_memory.write_uchar(0x0085A613, weight)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    PVZ_memory.write_uchar(0x008D0613, weight)
        elif PVZ_version == 2.3:
            if self.type <= 55:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 56:
                PVZ_memory.write_uchar(0x008D0882, weight)
            elif self.type == 57:
                PVZ_memory.write_uchar(0x008D0743, weight)
            elif self.type == 58:
                PVZ_memory.write_uchar(0x008D051C, weight)
            elif self.type == 59:
                PVZ_memory.write_uchar(0x008D05F7, weight)
        elif PVZ_version == 2.35 or PVZ_version == 2.36 or PVZ_version == 2.37:
            if self.type <= 58:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 59:
                PVZ_memory.write_uchar(0x008D0896, weight)
            elif self.type == 60:
                PVZ_memory.write_uchar(0x008D0743, weight)
            elif self.type == 61:
                PVZ_memory.write_uchar(0x008D051C, weight)
            elif self.type == 62:
                PVZ_memory.write_uchar(0x008D05F7, weight)
        elif PVZ_version == 2.4:
            if self.type <= 63:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 64:
                PVZ_memory.write_uchar(0x008D0896, weight)
            elif self.type == 65:
                PVZ_memory.write_uchar(0x008D0743, weight)
            elif self.type == 66:
                PVZ_memory.write_uchar(0x008D051C, weight)
            elif self.type == 67:
                PVZ_memory.write_uchar(0x008D05F7, weight)
        elif PVZ_version == 2.4:
            if self.type <= 65:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 66:
                PVZ_memory.write_uchar(0x008D0896, weight)
            elif self.type == 67:
                PVZ_memory.write_uchar(0x008D0743, weight)
            elif self.type == 68:
                PVZ_memory.write_uchar(0x008D051C, weight)
            elif self.type == 69:
                PVZ_memory.write_uchar(0x008D05F7, weight)


potted_size = 0x58


class potted:
    def __init__(self, addr):
        self.addr = addr
        self.no = (int)(
            (
                addr
                - 0x30000
                - PVZ_memory.read_uint(PVZ_memory.read_uint(0x6A9EC0) + 0x82C)
            )
            / 0x58
        )
        self.type = PVZ_memory.read_uint(self.addr)
        self.garden = PVZ_memory.read_uint(self.addr + 0x4)
        self.col = PVZ_memory.read_uint(self.addr + 0x8)
        self.row = PVZ_memory.read_uint(self.addr + 0xC)
        self.direction = PVZ_memory.read_uint(self.addr + 0x10)
        self.color = PVZ_memory.read_uint(self.addr + 0x20)
        self.state = PVZ_memory.read_uint(self.addr + 0x24)
        self.water = PVZ_memory.read_uint(self.addr + 0x28)
        self.waterMax = PVZ_memory.read_uint(self.addr + 0x2C)

    def setType(self, type):
        PVZ_memory.write_int(self.addr, type)

    def setGarden(self, garden):
        PVZ_memory.write_int(self.addr + 0x4, garden)

    def setCol(self, col):
        PVZ_memory.write_int(self.addr + 0x8, col)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr + 0xC, row)

    def setDirection(self, direction):
        PVZ_memory.write_int(self.addr + 0x10, direction)

    def setColor(self, color):
        PVZ_memory.write_int(self.addr + 0x20, color)

    def setState(self, state):
        PVZ_memory.write_int(self.addr + 0x24, state)

    def setWater(self, water):
        PVZ_memory.write_int(self.addr + 0x28, water)

    def setWaterMax(self, waterMax):
        PVZ_memory.write_int(self.addr + 0x2C, waterMax)
