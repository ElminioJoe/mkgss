from .models import Academic, Administration, Curricular, HomeFeature, Admission, SchoolValue, SchoolHistory


def create_home_feature_objects():
    HomeFeature.objects.create(
        welcome_info="Welcome to Moi Kadzonzo Girls High School website. It is designed for parents, students, Alumni, staff, sponsors, friends of the school and prospective parents who may know little about us.",
        administration_info="Meet our team of experienced professionals who manage and lead our organization. Our administration is dedicated to providing the best possible service to our clients and stakeholders.",
        academics_info="Our educational programs are designed to prepare students for success in their chosen careers. We offer a wide range of courses and programs, from technical training to liberal arts and sciences.",
        staff_info="Our staff is made up of dedicated and talented individuals who are committed to providing excellent service to our clients and customers. They bring a wealth of experience and expertise to their roles, ensuring that we deliver the highest quality work.",
        curricular_info="Our curricular activities are designed to provide students with opportunities to explore their interests, develop new skills, and build relationships with peers. We offer a wide range of activities, from sports teams and clubs to music and theater programs.",
        library_info="Our library is a vital resource for students and researchers, providing access to a wide range of books, journals, and digital resources. Our knowledgeable staff is available to assist with research and information inquiries.",
        alumni_info="Our alumni are an important part of our community, and we are proud of their accomplishments and contributions. We maintain strong relationships with our alumni, providing opportunities for networking, professional development, and social events."
    )


def create_school_info_objects():
    _, created = Administration.objects.get_or_create(
        name="Administration",
        defaults={
            "admin_info": "Administration information goes here"
        }
    )
    if created:
        print("Administration object created.")

    _, created = Admission.objects.get_or_create(
        name="Admission",
        defaults={
            "admission_info": "admission information goes here"
        }
    )
    if created:
        print("Admission object created.")

    _, created = Academic.objects.get_or_create(
        name="Academic",
        defaults={
            "academics_info": "academic information goes here"
        }
    )
    if created:
        print("Academic object created.")

    _, created = Curricular.objects.get_or_create(
        name="Curricular",
        defaults={
            "curricular_info": "Curricular information goes here"
        }
    )
    if created:
        print("Curricular object created.")

    _, created = SchoolValue.objects.get_or_create(
        name="School Values",
        defaults={
            "motto": "Bright Shining Star of Academic Excellence in the Nation.",
            "mission": "Instilling Self-Esteem And Empowering The Girl Child For The Competitive Market In Life.",
            "vision": "To Be A Bright Shining Star of Academic Excellence In The Nation.",
        }
    )
    if created:
        print("SchoolValue object created.")

    history_file = "home/school_history.txt"
    with open(history_file, "r") as f:
        history_content = f.read()

    _, created = SchoolHistory.objects.get_or_create(
        name="School History",
        defaults={
            "content": history_content
        }
    )
    if created:
        print("SchoolHistory object created.")


