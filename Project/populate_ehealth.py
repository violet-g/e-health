import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from ehealth.models import *

#zdravko is cool


def populate():

    Searcher.objects.all().delete()
    Folder.objects.all().delete()
    Page.objects.all().delete()
    for user in User.objects.all():
        if user.is_staff != True:
            user.delete()

    user1 = add_searcher("boris","boris@test.com","boris","boris","lazarov","true")
    user2 = add_searcher("zdravko","zdravko@test.com","zdravko","zdravko","ivanov","false")
    user3 = add_searcher("jill","jill@mail.com","jill","jill","valentine","true")
    user4 = add_searcher("bob","bob@mail.com","bob","bob","ross","false")
    user5 = add_searcher("jen","jen@mail.com","jen","jen","katarn","true")


    bFolder = add_folder(user1,"boris\'s folder","true")
    zFolder = add_folder(user2,"zdravko\'s folder","false")
    jillFolder = add_folder(user3,"My serious Ailments","false")
    jillFolder1 = add_folder(user3,"My other Ailments","true")
    bobFolder = add_folder(user4,"What sports do to you","true")
    bobFolder1 = add_folder(user4,"Problems","false")
    jenFolder = add_folder(user5,"My Folder","false")


    page = add_page("Eye Infections","MedlinePlus","Your eyes can get infections from bacteria, fungi, or viruses. Eye infections can occur in different parts of the eye and can affect just one eye or both. Two common eye infections are	Conjunctivitis - also known as pinkeye. Conjunctivitis is often due to an infection. Children frequently get it, and it is very contagious. Stye - a bump on the eyelid that happens when bacteria from your skin get into the hair follicle of an eyelash.Symptoms of eye infections may include redness, itching, swelling, discharge, pain, or problems with vision. Treatment depends on the cause of the infection and may include compresses, eye drops, creams, or antibiotics.",
                    "https://www.nlm.nih.gov/medlineplus/eyeinfections.html",66.74,48.75,41.5,0)

    page1 = add_page("Eye Diseases","MedlinePlus","Some eye problems are minor and don't last long. But some can lead to a permanent loss of vision.Common eye problems includeRefractive errorsCataracts - clouded lensesGlaucoma - a disorder caused by damage to the optic nerveRetinal disorders - problems with the nerve layer at the back of the eyeMacular degeneration - a disease that destroys sharp, central visionDiabetic eye problemsConjunctivitis - an  infection also known as pinkeyeYour best defense is to have regular checkups, because eye diseases do not always have symptoms. Early detection and treatment could prevent vision loss. See an eye care professional right away if you have a sudden change in vision, if everything looks dim, or if you see flashes of light. Other symptoms that need quick attention are pain, double vision, fluid coming from the eye, and inflammation.NIH: National Eye Institute ",
                     "https://www.nlm.nih.gov/medlineplus/eyediseases.html",44.75,55.4695767196,
                     31.4128001628,0)

    page2 = add_page("Amblyopia","MedlinePlus"," Amblyopia, or 'lazy eye,' is the most common cause of visual impairment in children.  It happens when an eye fails to work properly with the brain.  The eye may look normal, but the brain favors the other eye.   In some cases, it can affect both eyes.  Causes includeStrabismus - a disorder in which the two eyes don't line up in the same directionRefractive error in an eye - when one eye cannot focus as well as the other, because of a problem with its shape.  This includes nearsightedness, farsightedness, and astigmatism.Cataract - a clouding in the lens of the eyeIt can be hard to diagnose amblyopia.  It is often found during a routine vision exam.Treatment for amblyopia forces the child to use the eye with weaker vision.  There are two common ways to do this.  One is to have the child wear a patch over the good eye for several hours each day, over a number of weeks to months.  The other is with eye drops that temporarily blur vision.  Each day, the child gets a drop of a drug called atropine in the stronger eye.  It is also sometimes necessary to treat the underlying cause.  This could include glasses or surgery.NIH: National Eye Institute",
    "https://www.nlm.nih.gov/medlineplus/amblyopia.html",76.22,47.9166666667,43.3854166667,0)

    page3 = add_page("Arm Injuries and Disorders","MedlinePlus","Of the 206 bones in your body, 3 of them are in your arm; the humerus, radius and ulna. Your arms are also made up of muscles, joints, tendons and other connective tissue. Injuries to any of these parts of the arm can occur during sports, a fall or an accident.Types of arm injuries include Tendinitis and bursitisSprainsDislocationsBroken bonesSome nerve problems, arthritis, or cancers can affect the entire arm and cause pain, spasms, swelling and trouble moving. You may also have problems or injure specific parts of your arm, such as your hand, wrist, elbow or shoulder. ",
                     "https://www.nlm.nih.gov/medlineplus/arminjuriesanddisorders.html","60.65","46.75","36.5",0)

    page4 = add_page("Hip Replacement","MedlinePlus","Hip replacement is surgery for people with severe hip damage. The most common cause of damage is osteoarthritis. Osteoarthritis causes pain, swelling, and reduced motion in your joints. It can interfere with your daily activities. If other treatments such as physical therapy, pain medicines, and exercise haven't helped, hip replacement surgery might be an option for you.During a hip replacement operation, the surgeon removes damaged cartilage and bone from your hip joint and replaces them with new, man-made parts.A hip replacement canRelieve painHelp your hip joint work betterImprove walking and other movementsThe most common problem after surgery is hip dislocation. Because a man-made hip is smaller than the original joint, the ball can come out of its socket. The surgery can also cause blood clots and infections. With a hip replacement, you might need to avoid certain activities, such as jogging and high-impact sports.NIH: National Institute of Arthritis and Musculoskeletal and Skin Diseases",
                     "https://www.nlm.nih.gov/medlineplus/hipreplacement.html",49.82,53.1273191095,44.0630797774,0)

    page5 = add_page("Get Tested for Colorectal Cancer","Healthfinder","Get tested regularly for colorectal cancer starting at age 50. All it takes is a special exam (called a screening). Talk to other people who have been tested to learn what to expect.",
                     "http://healthfinder.gov/HealthTopics/Category/doctor-visits/screening-tests/get-tested-for-colorectal-cancer",77.23,52.9017857143,28.0837912088,0)

    page6 = add_page("Take Steps to Prevent Skin Cancer","Healthfinder","Ultraviolet (UV) radiation from the sun is the main cause of skin cancer. Check your skin regularly for any new growths or other changes.",
                     "http://healthfinder.gov/HealthTopics/Category/parenting/safety/steps-to-prevent-skin-cancer","76.22","52.2253787879","30.99504662",0)

    page7 = add_page("Stubbed Toe - Diagnosis & Treatment Options For You","Bing","Learn when to seek treatment for a stubbed toe and what you can do to minimize pain, swelling, and other symptoms that may appear for stubbed toes.",
                     "http://www.footvitals.com/toes/stubbed-toe.html",77.91,43.75,37.5,0)



    folderContent1 = add_pageFolder(page1,bFolder)
    folderContent2 = add_pageFolder(page2,bFolder)
    folderContent3 = add_pageFolder(page1,zFolder)

    folderContent4 = add_pageFolder(page1,jillFolder)
    folderContent5 = add_pageFolder(page,jillFolder)
    folderContent6 = add_pageFolder(page7,jillFolder1)
    folderContent7 = add_pageFolder(page3,bobFolder)
    folderContent8 = add_pageFolder(page4,bobFolder)
    folderContent9 = add_pageFolder(page5,bobFolder1)
    folderContent10 = add_pageFolder(page6,jenFolder)


def add_page(title,source,summary,url,readability_score,sentiment_score,
             subjectivity_score,times_saved):
    newPage = Page(title=title,source=source,summary=summary,url=url,readability_score=readability_score,sentiment_score=sentiment_score,subjectivity_score=subjectivity_score,times_saved=times_saved)
    newPage.save()
    return newPage

def add_folder(user,name,public):
    newFolder = Folder(user=user,name=name,public=public)
    newFolder.save()
    return newFolder

def add_searcher(username,email,password,first_name,last_name,public):
        newuser = User.objects.create_user(username=username, email=email, password = password,first_name=first_name,last_name=last_name )
        newuser.save()
        newSearcher = Searcher(user = User.objects.get(username=username))
        newSearcher.public = public
        newSearcher.save()
        return newSearcher

def add_pageFolder(page,folder):
    relationship = FolderPage(folder=folder,page=page)
    relationship.save()
    return relationship


# Start execution here!
if __name__ == '__main__':
    print "Starting Ehealth population script..."
    populate()
    print "Ehealth population script successfully completed."
