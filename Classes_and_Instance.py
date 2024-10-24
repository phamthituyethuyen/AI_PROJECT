''' __dict__ is function to show all attribute of instance or itsell class
    For example: print(Employee1.__dict__) or print(Employee.__dict__)'''


class Employee:
    raise_of_mount = 1.02
    def __init__(self,fist_name, Id_student):
        self.fist_name = fist_name
        self.Id_student = Id_student
        self.mail = fist_name + Id_student +"@gmail.com"
        
    def information(self):
        return '1.{} \n2.{} \n3.{}'.format(self.fist_name, self.Id_student,self.mail)
    
    def mount_of_employ(self):
        return float(self.Id_student) * Employee.raise_of_mount
    
    @classmethod
    def set_raise_mount(cls, mount):
        cls.Id_student = mount
        return
    
    #Khong cần dùng self
    @staticmethod
    def notice_infor():
        print("thong tin chua duoc cap nhat")

        

# Regular method    
Employee1 = Employee("tuyethuyenpham", "21166127")
print(Employee1.information())
print('The salary of {} is: {}'.format(Employee1.fist_name, int(Employee1.mount_of_employ())))

# class method
Employee.set_raise_mount(15)
Employee2 = Employee("huyen", "2166127")
print(Employee2.information())

#static method
Employee2.notice_infor()

print(dir(int))