import struct

class Student:
    def __init__ (self, rollno, name, dept, sem, prcnt, phone):
        self.rollno = rollno
        self.name = name
        self.dept = dept
        self.sem = sem
        self.prcnt = prcnt
        self.phone = phone
class Grade:
    def __init__ (self, course, rollno, prcnt):
        self.course = course
        self.rollno = rollno
        self.prcnt = prcnt
def pack (rollno, name, dept, sem, prcnt, phone):
    f = '11s 30s 2s I f 11s'
    rollno = rollno.encode('utf-8')
    name = name.encode('utf-8')
    dept = dept.encode('utf-8')
    phone = phone.encode('utf-8')
    return struct.pack (f, rollno, name, dept, sem, prcnt, phone)
def pack_grade (course, rollno, prcnt):
    f = '20s 11s f'
    course = course.encode()
    rollno = rollno.encode()
    return struct.pack (f, course, rollno, prcnt)
def unpack (data):
    f = '11s 30s 2s I f 11s'
    return struct.unpack (f,data)
def format_student_data (data):
    print(data[0].decode(),data[1].decode(),data[2].decode(),data[3],data[4],data[5].decode())
def format_grade_data (data):
    print(data[0].decode(),data[1].decode(),data[2])
def check_dup_rollno (file,rollno):
    file.seek(0)
    f = '11s 30s 2s I f 11s'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        var_rollno = unpacked_data[0].decode().strip('\x00')
        if var_rollno == rollno:
            return True
    return False
def calcAverage (file,course):
    file.seek(0)
    f = '20s 11s f'
    sum_ = 0
    num = 0
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        prcnt = unpacked_data[2]
        sum_ += prcnt
        num += 1
    return sum_ // num
def calcHighest (file,course):
    file.seek(0)
    f = '20s 11s f'
    marks_list = []
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        prcnt = unpacked_data[2]
        marks_list.append(prcnt)
    return max(marks_list)
def calcLowest (file,course):
    file.seek(0)
    f = '20s 11s f'
    marks_list = []
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        prcnt = unpacked_data[2]
        marks_list.append(prcnt)
    return min(marks_list)
def add_student (file, obj):
    rollno = obj.rollno
    name = obj.name
    dept = obj.dept
    sem = obj.sem
    prcnt = obj.prcnt
    phone = obj.phone
    data = pack(rollno, name, dept, sem, prcnt, phone)
    file.write (data)
    print('Student Added Successfully')
def view_student (file,rollno):
    file.seek(0)
    f = '11s 30s 2s I f 11s'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            print('Student Not Found')
            return False
            break
        unpacked_data = struct.unpack(f,data)
        var_rollno = unpacked_data[0].decode().strip('\x00')
        if var_rollno == rollno:
            format_student_data(unpacked_data)
            break
def edit_student (file,rollno):
    file.seek(0)
    f = '11s 30s 2s I f 11s'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            print('Student Not Found')
            break
        unpacked_data = struct.unpack(f,data)
        var_rollno = unpacked_data[0].decode().strip('\x00')
        if var_rollno == rollno:
            new_data = pack (input('Enter new Rollno: '),input('Enter new Name: '),input('Enter new Department: '),int(input('Enter new Semester: ')),float(input('Enter new Percentage: ')),input('Enter new Phone No.: '))
            file.seek(-struct.calcsize(f),1)
            file.write(new_data)
            print('Student Edited Successfully')
            break
def delete_student (file,rollno):
    file.seek(0)
    f = '11s 30s 2s I f 11s'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            print('Student Not Found')
            break
        unpacked_data = struct.unpack(f,data)
        var_rollno = unpacked_data[0].decode().strip('\x00')
        if var_rollno == rollno:
            file.seek(-struct.calcsize(f),1)
            deleted_data = pack('-' * 11, '-' * 30, '-' * 2, 0, 0.0, '-' * 11)
            file.write(deleted_data)
            print('Student Deleted Successfully')
            break
def student_list(file):
    file.seek(0)
    f = '11s 30s 2s I f 11s'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f, data)
        if all(c == '-' for c in data):
            continue
        format_student_data(unpacked_data)
def list_by_semester(file,sem):
    file.seek(0)
    f = '11s 30s 2s I f 11s'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        var_sem = unpacked_data[3]
        if var_sem == sem:
           format_student_data(unpacked_data)
def list_by_name(file,name):
    file.seek(0)
    f = '11s 30s 2s I f 11s'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        var_name = unpacked_data[1].decode().strip('\x00')
        if var_name == name:
            format_student_data(unpacked_data)
def check_dup_grade (file,course,rollno):
    file.seek(0)
    f = '20s 11s f'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        var_course = unpacked_data[0].decode().strip('\x00')
        var_rollno = unpacked_data[1].decode().strip('\x00')
        if var_rollno == rollno and var_course == course:
            return True
    return False
def add_grade(file, obj):
    course = obj.course
    rollno = obj.rollno
    prcnt = obj.prcnt
    data = pack_grade(course,rollno,prcnt)
    file.write (data)
def view_grades (file, rollno):
    file.seek(0)
    f = '20s 11s f'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            print('Grades Not Found')
            break
        unpacked_data = struct.unpack(f,data)
        var_rollno = unpacked_data[1].decode().strip('\x00')
        if var_rollno == rollno:
            format_grade_data(unpacked_data)
            break
def edit_grades (file,rollno):
    file.seek(0)
    f = '20s 11s f'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            print('Grades Not Found')
            break
        unpacked_data = struct.unpack(f,data)
        var_rollno = unpacked_data[1].decode().strip('\x00')
        if var_rollno == rollno:
            new_data = pack_grade(unpacked_data[0].decode().strip('\x00'),unpacked_data[1].decode().strip('\x00'),float(input('Enter new Percentage: ')))
            file.seek(-struct.calcsize(f),1)
            file.write(new_data)
            print('Grade Edited Successfully')
            break
def delete_grades(file,rollno,course):
    file.seek(0)
    f = '20s 11s f'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            print('Grades Not Found')
            break
        unpacked_data = struct.unpack(f,data)
        var_rollno = unpacked_data[1].decode().strip('\x00')
        var_course = unpacked_data[0].decode().strip('\x00')
        if var_rollno == rollno and var_course == course:
            file.seek(-struct.calcsize(f),1)
            deleted_data = pack_grade('-' * 20, '-' * 11,0.0)
            file.write(deleted_data)
            print('Grade Deleted Successfully')
            break
def list_grades_by_student(file,rollno):
    file.seek(0)
    f = '20s 11s f'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        var_rollno = unpacked_data[1].decode().strip('\x00')
        if var_rollno == rollno:
            format_grade_data(unpacked_data)
def list_grades_by_course(file,course):
    file.seek(0)
    f = '20s 11s f'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        var_course = unpacked_data[0].decode().strip('\x00')
        if var_course == course:
            format_grade_data(unpacked_data)
def generate_award_sheet (file):
    course_list=[]
    file.seek(0)
    f = '20s 11s f'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        course = unpacked_data[0].decode().strip('\x00')
        if course not in course_list:
            course_list.append(course)
    for course in course_list:
        if course != '--------------------':
            print(f"Course Name: {course}\n\n")
            list_grades_by_course(file,course)
        print('\n\n')
def generate_course_list (file):
    course_list=[]
    file.seek(0)
    f = '20s 11s f'
    while True:
        data = file.read(struct.calcsize(f))
        if not data:
            break
        unpacked_data = struct.unpack(f,data)
        course = unpacked_data[0].decode().strip('\x00')
        if course not in course_list:
            course_list.append(course)
    return course_list
def generate_summary_sheet (file):
    course_list=generate_course_list(file)
    for course in course_list:
        print(f"Course Name: {course}\n\n")
        list_grades_by_course(file,course)
        print()
        print(f'Average Marks in {course}: ',calcAverage(file,course))
        print(f'Highest Marks in {course}: ',calcHighest(file,course))
        print(f'Lowest Marks in {course}: ',calcLowest(file,course))
def generate_transcript (file1,file2,rollno):
    file1.seek(0)
    file2.seek(0)
    f1 = '11s 30s 2s I f 11s'
    f2 = '20s 11s f'
    while True:
        data_1 = file1.read(struct.calcsize(f1))
        data_2 = file2.read(struct.calcsize(f2))
        if not data_1:
            break
        if not data_2:
            break
        unpacked_data_1 = struct.unpack(f1,data_1)
        unpacked_data_2 = struct.unpack(f2,data_2)
        var_rollno = unpacked_data_2[1].decode().strip('\x00')
        name = unpacked_data_1[1].decode('utf-8')
        
        if var_rollno == rollno:
            print(f"Student Name: {name}\t\t")
            print(f"Student Roll Number: {rollno}\n\n")
            list_grades_by_student(file2,rollno)
                
            
def main ():
    print('\t\tWelcome to PUCIT Database Managament System')
    print()
    print()
    print('1. Quit the management system')
    print('2. Add a Student')
    print('3. View Student by Roll Number')
    print('4. Edit Student by Roll Number')
    print('5. Delete Student by Roll Number')
    print('6. List Students by Semester')
    print('7. List Students by Name')
    print('8. Print Students List')
    print('9. Add Grade of a Student for a Course')
    print('10. Import Grades')
    print('11. View Grades of a Student')
    print('12. Edit Grades of a Student for a Course: ')
    print('13. Delete Grades of a Student for a Course: ')
    print('14. List Student Wise Grades of Courses: ')
    print('15. List Course Wise Grades of Students: ')
    print('16. Generate Award Sheet')
    print('17. Generate Summary Sheet')
    print('18. Generate Transcript')
    print('\n\n\n')
    
    file1 = open('student.bin', 'rb+')
    file2 = open('grades.bin', 'rb+')
    
    while True:
        func = input('Enter Function to perform (number): ')
        print()
        if func == '1':
            print('\nQuiting...............................')
            break
        elif func == '2':
            rollno = input('Enter Roll Number of Student: ')
            if check_dup_rollno (file1, rollno):
                print('Student already exists')
            else:
                name = input('Enter Name of Student: ')
                dept = input('Enter Department of Student: ')
                sem = int(input('Enter Semester of Student: '))
                prcnt = float(input('Enter Previous Semester Percentage:  '))
                phone = input('Enter Phone Number of Student: ')
                obj = Student(rollno,name,dept,sem,prcnt,phone)
                add_student(file1,obj)
        elif func == '3':
            view_student (file1, input('Enter Roll Number: '))
        elif func == '4':
            edit_student(file1, input('Enter Roll Number: '))
        elif func == '5':
            delete_student(file1, input('Enter Roll Number: '))
        elif func == '6':
            list_by_semester(file1,int(input('Enter Semester: ')))
        elif func == '7':
            list_by_name(file1,input('Enter Name: '))
        elif func == '8':
            student_list(file1)
        elif func == '9':
            course = input('Enter Course Name: ')
            rollno = input('Enter Roll Number of Student: ')
            if check_dup_grade (file2,course,rollno):
                print('Record already exists')
            else:
                prcnt = float(input('Enter Percentage:  '))
                obj = Grade (course,rollno,prcnt)
                add_grade(file2,obj)
        elif func == '10':
            pass
        elif func == '11':
            view_grades(file2, input('Enter Roll Number of Student: '))
        elif func == '12':
            edit_grades (file2,input('Enter Roll Number of Student: '))
        elif func == '13':
            delete_grades(file2, input('Enter Roll Number of Student: '), input('Enter Course Name: '))
        elif func == '14':
            list_grades_by_student(file2, input('Enter Roll Number of Student: '))
        elif func == '15':
            list_grades_by_course(file2, input('Enter Course Name: '))
        elif func == '16':
            generate_award_sheet(file2)
        elif func == '17':
            generate_summary_sheet (file2)
        elif func == '18':
            rollno = input('Enter Roll Number of Student: ')
            generate_transcript (file1,file2,rollno)
        else:
            print('Invalid Command!!!!!!!!\n')

        print()
        
            
main()
        
