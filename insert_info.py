from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item, User

engine = create_engine('sqlite:///superclimbing.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')  # noqa
session.add(User1)
session.commit()

# Menu for Super-Climbing
category1 = Category(user_id=1, name="Bouldering", description="""Bouldering is a form of rock climbing
 that is performed on small rock formations or artificial rock walls,
 known as boulders, without the use of ropes or harnesses. While it can be done
 without any equipment, most climbers use climbing shoes to help secure
 footholds, chalk to keep their hands dry and provide a firmer grip,
 and bouldering mats to prevent injuries from falls.""",
                     cat_image_filename="Bouldering.jpg",
                     cat_image_url="http://localhost:8000/static/img/Bouldering.jpg")  # noqa

session.add(category1)
session.commit()

Item1 = Item(name="Edge Climbing Shoe", description="""Versatile shoe excels on slab, crack, and face climbs
P3 technology maintains a moderate downturn for life
Vibram XS Edge optimizes edging performance
Leather upper conforms to your foot shape for comfort
Lorica lacing system minimizes stretch for an exact fit""",
             price="$185.50", category=category1,
             item_image_filename="climbing_shoe.jpg",
             item_image_url="http://localhost:8000/static/img/climbing_shoe.jpg")  # noqa

session.add(Item1)
session.commit()

Item2 = Item(name="Super Chalk, 5 oz", description="""In the storm of flashy hardware, it
is sometimes easy to overlook other climbing necessities such as chalk.
Super Chalk features a safe drying agent to help maximize your grip
when the vertical world is trying to spit you out. The chalk comes in
a resealable bag to make transport easy and mess-free.""",
             price="$4.99", category=category1,
             item_image_filename="super_chalk.jpg",
             item_image_url="http://localhost:8000/static/img/super_chalk.jpg")

session.add(Item2)
session.commit()

Item3 = Item(name="Unicorn dust, 10 oz", description="""Ultra-fine chalk dust for sending the gnarliest climbs
No unnecessary fillers, only chalk for sticking the moves
Finely ground for easy application""", price="$24.50", category=category1,
             item_image_filename="unicorn_dust.jpg",
             item_image_url="http://localhost:8000/static/img/unicorn_dust.jpg")  # noqa

session.add(Item3)
session.commit()

Item4 = Item(name="BPLUS chalk bag", description="""Chalk bag for monstrous climbing routes
Soft pile lining for ideal chalk distribution
Stiffened rim for easy dipping
Brush holders on monster arms
Drawstring closure seals chalk in""", price="$30.99", category=category1,
             item_image_filename="chalk_bag.jpg",
             item_image_url="http://localhost:8000/static/img/chalk_bag.jpg")

session.add(Item4)
session.commit()

category2 = Category(user_id=1, name="Trad & Aid climbing", description="""Aid climbing is a style of climbing
 in which standing on or pulling oneself up via devices attached to fixed
 or placed protection is used to make upward progress.The term contrasts with
 free climbing in which progress is made without using artificial aids: a free
 climber ascends by only holding onto and stepping on natural features of the
 rock, using rope and equipment merely to catch them in case of fall and
 provide belay.""", cat_image_filename="rock_climbing.jpg",
                     cat_image_url="http://localhost:8000/static/img/rock_climbing.jpg")  # noqa

session.add(category2)
session.commit()

Item5 = Item(name="Gigri 2 Belay Device", description="""Durable stainless steel cam and friction plates
stand up to years of use. Easy-to-read diagrams on the aluminum side plates
help you make sure you're set up correctly. Assisted braking system helps
check your partner's fall when he skips one clip and botches the next.
Brake handle gives you excellent control for lowering. Designed to accommodate
rope diameters between 8.9 and 11 millimeters; ideal rope diameters are between
9.4 to 10.3 millimeter""",
             price="$97.99",
             category=category2,
             item_image_filename="gigri_belay.jpg",
             item_image_url="http://localhost:8000/static/img/gigri_belay.jpg")

session.add(Item5)
session.commit()

Item6 = Item(name="DMM Phantom Carabiner - 6 pack", description="""Each of your carabiners may only
weigh a few ounces, but multiply that by your fifty cams and you're carrying
a rather rotund child in 'biners alone. The DMM Phantom Carabiner 6 Pack trims
the fat to help increase your efficiency for demanding traditional
and aid climbing. The Phantom uses DMM's I-Beam technology
(the spine resembles a steel I-beam) and a lightweight alloy for strength and
weight reduction, and the custom bent wire gate pulls itself
into the nose when weighted.""", price="$40.99", category=category2,
             item_image_filename="dmm_phantom.jpg",
             item_image_url="http://localhost:8000/static/img/dmm_phantom.jpg")

session.add(Item6)
session.commit()

Item7 = Item(name="Meteor Climbing Helmet", description="""A lightweight helmet designed for climbing
and mountaineering. Well ventilated design keeps cool air circulating through
Breathable foam stabilizes helmet while climbing
Headband and chinstrap are adjustable for a snug fit
Integrated clips secure headlamps around helmet""", price="$97.99",
             category=category2, item_image_filename="meteor_helmet.jpg",
             item_image_url="http://localhost:8000/static/img/meteor_helmet.jpg")  # noqa

session.add(Item7)
session.commit()

Item8 = Item(name="Corax Harness", description="""Versatile climbing harness for rock, ice, alpine,
or via ferrata. Frame Construction Technology for durability and comfort
DoubleBack buckles at waist and legs for adjustable fit
Four gear loops and two ice attachments for massive storage""", price="$54.99",
             category=category2, item_image_filename="corax_harness.jpg",
             item_image_url="http://localhost:8000/static/img/corax_harness.jpg")  # noqa

session.add(Item8)
session.commit()

Item9 = Item(name="Classic Climbing Rope - 9.5mm 40m", description="""Classic climbing rope for
the versatile rock climber. Skinny 9.5mm diameter for intermediate to
advanced handling""", price="$94.99", category=category2,
             item_image_filename="climbing_rope.jpg",
             item_image_url="http://localhost:8000/static/img/climbing_rope.jpg")  # noqa

session.add(Item9)
session.commit()

category3 = Category(user_id=1, name="Ice Climbing", description="""Ice climbing is the activity of ascending inclined ice
 formations. Usually, ice climbing refers to roped and protected
 climbing of features such as icefalls, frozen waterfalls, and cliffs
 and rock slabs covered with ice refrozen from flows of water.
 For the purposes of climbing, ice can be broadly divided into two spheres,
 alpine ice and water ice. Alpine ice is found in a mountain environment,
 usually requires an approach to reach, and is often climbed in an attempt
 to summit a mountain. Water ice is usually found on a cliff or other
 outcropping beneath water flows""", cat_image_filename="ice_climbing.jpg",
                     cat_image_url="http://localhost:8000/static/img/ice_climbing.jpg")  # noqa

session.add(category3)
session.commit()

Item10 = Item(name="Express Ice Screws", description="""Express Ice Screws' unique taper reduces
ice fracturing and eases placements. Dual clip in points make belays
much easier to build. Tapered design for easier placements """,
              price="$60.92", category=category3,
              item_image_filename="express_ice_screws.jpg",
              item_image_url="http://localhost:8000/static/img/express_ice_screws.jpg")  # noqa

session.add(Item10)
session.commit()

Item11 = Item(name="Cobra Ice Tool", description="""Carbon fiber shaft dampens your swing for
more one swing sticks. Carbon fiber shaft doesn't chill your hand like aluminum
Choke-up spur allows easier matching on steep terrain""",
              price="$184.76", category=category3,
              item_image_filename="cobra_ice_tool.jpg",
              item_image_url="http://localhost:8000/static/img/cobra_ice_tool.jpg")  # noqa

session.add(Item11)
session.commit()

Item12 = Item(name="Icefall Gauntlet Glove", description="""Event membrane
Matrix stretch areas
PrimaLoft Gold insulation
Pittards Armortan leather palm
Drawcord gauntlet closure
Detachable wrist leashes
Flocking patch at back of thumb""", price="$132.00", category=category3,
              item_image_filename="ice_glove.jpg",
              item_image_url="http://localhost:8000/static/img/ice_glove.jpg")

session.add(Item12)
session.commit()

Item13 = Item(name="Dyneema Ice 40L Backpack", description="""Removable aluminum stays
Foam back panel, shoulder straps, and waist belt
Roll-top closure
External crampon and ice axe attachment system
Internal zippered pocket
Four side compression system""", price="$440.46", category=category3,
              item_image_filename="ice_backpack.jpg",
              item_image_url="http://localhost:8000/static/img/ice_backpack.jpg")  # noqa

session.add(Item13)
session.commit()

category4 = Category(user_id=1, name="Climbing Training", description="""Climbing training is at a crossroads.
Unprecedented access to thousands of square feet of indoor terrain means
climbers are stronger than ever-weather, temps, and daylight are no longer
factors. However, real science behind climbing training is in its infancy""",
                     cat_image_filename="climbing_training.jpg",
                     cat_image_url="http://localhost:8000/static/img/climbing_training.jpg")  # noqa

session.add(category4)
session.commit()
print ("All set up!")
