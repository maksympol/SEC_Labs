import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PyQt5 import QtCore
from design import Ui_Lab1_security
import os, stat, shutil, getpass, json, re, time


class Window(QMainWindow, Ui_Lab1_security):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.connectSignalsSlots()


    def connectSignalsSlots(self):
        self.button_start.clicked.connect(self.start_function)
        self.button_end.clicked.connect(self.end_function)
        self.button_pwd.clicked.connect(self.pwd)
        self.button_cd.clicked.connect(self.cd)
        self.button_ls.clicked.connect(self.ls)
        self.button_mkdir.clicked.connect(self.mkdir)
        self.button_rmdir.clicked.connect(self.rmdir)
        self.button_vi.clicked.connect(self.vi)
        self.button_rmfile.clicked.connect(self.rmfile)


    def update_paths(self):
        global lst_paths, lst_directories, lst_files, index, directories, first_work_directory, len_first_work_path, wd, start_time
        lst_paths = []
        lst_directories = []
        lst_files = []
        index = 0
        first_work_directory = "Dir0/"
        last_work_directory = r"Dir1/Dir2/Dir3/Dir4"
        directories = first_work_directory + last_work_directory
        if Window.iter_start == 0:
            wd = os.getcwd()
            Window.start_time = time.time()
            Window.iter_start += 1
        all_directory = wd
        first_work_path = all_directory.replace(last_work_directory, '')
        len_first_work_path = len(first_work_path)
        for path, directory, file in os.walk(top=f"{first_work_path}/{first_work_directory}"):
            try:
                file.remove("login-password.json")
                lst_paths.append(path)
                lst_files.append(file)
                lst_directories.append(directory)

            except ValueError:
                lst_paths.append(path)
                lst_files.append(file)
                lst_directories.append(directory)
            
        print("Paths are updated!")

    iter_start = 0

    def ask_about_2_or_3_choice(self):
        global add_delete_user, start_time
        add_delete_user = input("\nInput 0, if you want to delete user.\nInput 1, if you want to add/modify user.\nInput 2, if you want to use the file system.\nInput 3, if you want to exit.\n")
        if add_delete_user == "2":
            if time.time() - Window.start_time > 20:
                question = input(f"\n{dict_password_login[login][2]}\n")
                if question != dict_password_login[login][3]:
                    sys.exit()
                else:
                    Window.start_time = time.time()
                    print(f"Good luck, {login}!")
                    self.label_choose_role.setText(f"You are admin ({login})")
                    Window.update_paths(self)
                    return True

            else:
                print(f"Good luck, {login}!")
                self.label_choose_role.setText(f"You are admin ({login})")
                Window.update_paths(self)
                return True

        elif add_delete_user == "3":
            print(f"Exit successful!")
            sys.exit()
            Window.update_paths(self)
            return True

        else:
            if time.time() - Window.start_time > 20:
                question = input(f"{dict_password_login[login][2]}")
                if question != dict_password_login[login][3]:
                    sys.exit()
                else:
                    Window.start_time = time.time()
                    Window.update_paths(self)
                    return False
            else:
                Window.update_paths(self)
                return False


    def create_directories(self):
        global first_work_directory, last_work_directory, directories, all_directory, first_work_path
        first_work_directory = "Dir0/"
        last_work_directory = r"Dir1/Dir2/Dir3/Dir4"
        directories = first_work_directory + last_work_directory
        all_directory = wd
        first_work_path = all_directory.replace(last_work_directory, '')
        try:
            os.makedirs(directories)
        except FileExistsError:
            pass

        for i in range(5):
            file = open(f"Dir{i}/dir{i}.txt", "w+")
            os.chdir(f"Dir{i}")
            file.write(f"Directory{i}")
            file.close()

        Window.update_paths(self)

    start_time = time.time()

    def start_function(self):
        global directories, all_directory, first_work_directory, last_work_directory, first_work_path, login, wd, dict_password_login, start_time
        if Window.iter_start == 0:
            wd = os.getcwd()
            Window.start_time = time.time()
            Window.iter_start += 1

        if os.path.exists(f"{wd}/Dir0/login-password.json"):
            login = getpass.getpass("Please, input your login: ")
            password = getpass.getpass("Please, input your password: ")

            try:
                with open(f"{wd}/Dir0/login-password.json", "r") as file:
                    dict_password_login = {k: v for k, v in json.load(file).items()}
                if dict_password_login[login][1] == "admin" and dict_password_login[login][0] == password:
                    first = Window.ask_about_2_or_3_choice(self)
                    
                    while first == False:
                        if add_delete_user == "0":
                            if time.time() - Window.start_time > 20:
                                question = input(f"\n{dict_password_login[login][2]}\n")
                                if question != dict_password_login[login][3]:
                                    sys.exit()
                                else:
                                    Window.start_time = time.time()
                                    login = input("Input login: ")
                                    if len(dict_password_login) > 1:
                                        dict_password_login.pop(login)
                                    else:
                                        dict_password_login.pop(login)
                                        os.remove(f"{wd}/Dir0/login-password.json")
                                        sys.exit()

                                    with open(f"{wd}/Dir0/login-password.json", "w", encoding="utf-8") as file:
                                        json.dump(dict_password_login, file)
                                    first = Window.ask_about_2_or_3_choice(self)
                            else:
                                login = input("Input login: ")
                                if len(dict_password_login) > 1:
                                    dict_password_login.pop(login)
                                else:
                                    dict_password_login.pop(login)
                                    os.remove(f"{wd}/Dir0/login-password.json")
                                    sys.exit()

                                with open(f"{wd}/Dir0/login-password.json", "w", encoding="utf-8") as file:
                                    json.dump(dict_password_login, file)
                                first = Window.ask_about_2_or_3_choice(self)

                        elif add_delete_user == "1":
                            if time.time() - Window.start_time > 20:
                                question = input(f"\n{dict_password_login[login][2]}\n")
                                if question != dict_password_login[login][3]:
                                    sys.exit()
                                else:
                                    Window.start_time = time.time()
                                    login = input("Input login: ")
                                    password = input("Input password: ")
                                    input_role = input("Input role: ")
                                    security_question = input("Input security question: ")
                                    security_answer = input("Input security answer: ")
                                    dict_password_login.update({login: [password, input_role, security_question, security_answer]})
                                    with open(f"{wd}/Dir0/login-password.json", "w", encoding="utf-8") as file:
                                        json.dump(dict_password_login, file)
                                    first = Window.ask_about_2_or_3_choice(self)
                            else:
                                login = input("Input login: ")
                                password = input("Input password: ")
                                input_role = input("Input role: ")
                                security_question = input("Input security question: ")
                                security_answer = input("Input security answer: ")
                                dict_password_login.update({login: [password, input_role, security_question, security_answer]})
                                with open(f"{wd}/Dir0/login-password.json", "w", encoding="utf-8") as file:
                                    json.dump(dict_password_login, file)
                                first = Window.ask_about_2_or_3_choice(self)

                        else:
                            print("Error choice!")

                elif dict_password_login[login][1] == "user" and dict_password_login[login][0] == password:
                    print(f"Good luck, {login}!")
                    self.label_choose_role.setText(f"You are user ({login})")

                else:
                    print("Autorization failed, login or/and password is incorrect!")
                    sys.exit()

            except Exception as exc:
                print("Exception is: ", exc)
                sys.exit()

            Window.create_directories(self)
            Window.update_paths(self)

        else:
            os.makedirs(f"{wd}/Dir0")
            with open(f"{wd}/Dir0/login-password.json", "w") as file:
                Window.create_directories(self)
                login = getpass.getpass("Please, input admin login: ")
                password = getpass.getpass("Please, input admin password: ")
                security_question = input("Input admin security question: ")
                security_answer = input("Input admin security answer: ")
                data = [password, "admin", security_question, security_answer]
                to_json = {login: data}
                os.chdir(f"{first_work_path}")
                with open(f"{wd}/Dir0/login-password.json", "w", encoding="utf-8") as file:
                    json.dump(to_json, file)
                print("Reloading system!")
                Window.update_paths(self)
                sys.exit()

        Window.iter_start += 1


    def end_function(self):
        sys.exit()


    def pwd(self):
        global lst_paths, index, start_time
        if time.time() - Window.start_time > 20:
            question = input(f"\n{dict_password_login[login][2]}\n")
            if question != dict_password_login[login][3]:
                sys.exit()
            else:
                Window.start_time = time.time()
                if Window.iter_start == 0:
                    self.line_edit_pwd.clear()
                    self.line_edit_pwd.setText("Permission denied!")
                else:
                    self.line_edit_pwd.clear()
                    self.line_edit_pwd.setText(lst_paths[index][len_first_work_path + 1::])
        else:
            if Window.iter_start == 0:
                self.line_edit_pwd.clear()
                self.line_edit_pwd.setText("Permission denied!")
            else:
                self.line_edit_pwd.clear()
                self.line_edit_pwd.setText(lst_paths[index][len_first_work_path + 1::])


    def ls(self):
        global lst_directories, lst_files, index, start_time
        if time.time() - Window.start_time > 20:
            question = input(f"\n{dict_password_login[login][2]}\n")
            if question != dict_password_login[login][3]:
                sys.exit()
            else:
                Window.start_time = time.time()
                if Window.iter_start == 0:
                    self.line_edit_ls.clear()
                    self.line_edit_ls.setText("Permission denied!")
                else:
                    self.line_edit_ls.clear()
                    self.line_edit_ls.setText(f"{lst_directories[index]} {lst_files[index]}")
        else:
            if Window.iter_start == 0:
                self.line_edit_ls.clear()
                self.line_edit_ls.setText("Permission denied!")
            else:
                self.line_edit_ls.clear()
                self.line_edit_ls.setText(f"{lst_directories[index]} {lst_files[index]}")


    def cd(self):
        global index, lst_paths, start_time
        Window.update_paths(self)

        text_cd = lst_paths[index][:len_first_work_path + 1] + self.line_edit_cd.text()
        if time.time() - Window.start_time > 20:
            question = input(f"\n{dict_password_login[login][2]}\n")
            if question != dict_password_login[login][3]:
                sys.exit()
            else:
                Window.start_time = time.time()

                if Window.iter_start == 0:
                    self.line_edit_cd.clear()
                    self.line_edit_cd.setText("Permission denied!")
                
                elif text_cd in lst_paths:
                    os.chdir(text_cd)
                    self.line_edit_cd.setText("Ok!")
                    index = lst_paths.index(text_cd)
                else:
                    self.line_edit_cd.setText("Error in path!")
        else:
            if Window.iter_start == 0:
                self.line_edit_cd.clear()
                self.line_edit_cd.setText("Permission denied!")
            
            elif text_cd in lst_paths:
                os.chdir(text_cd)
                self.line_edit_cd.setText("Ok!")
                index = lst_paths.index(text_cd)
            else:
                self.line_edit_cd.setText("Error in path!")


    def mkdir(self):
        global lst_paths, start_time
        Window.update_paths(self)

        text_mkdir = lst_paths[index][:len_first_work_path + 1] + self.line_edit_mkdir.text()
        match = re.findall(r"You are (.{4,12}) \(", self.label_choose_role.text())[0]

        if time.time() - Window.start_time > 20:
            question = input(f"\n{dict_password_login[login][2]}\n")
            if question != dict_password_login[login][3]:
                sys.exit()
            else:
                Window.start_time = time.time()

                if Window.iter_start == 0 and match != "admin":
                    self.line_edit_mkdir.clear()
                    self.line_edit_mkdir.setText("Permission denied!")

                elif text_mkdir not in lst_paths:
                    try:
                        os.mkdir(text_mkdir)
                        self.line_edit_mkdir.clear()
                        self.line_edit_mkdir.setText("Ok!")
                        Window.update_paths(self)
                        
                    except Exception as exc:
                        self.line_edit_mkdir.setText(f"{exc}")
                        Window.update_paths(self)

                else:
                    self.line_edit_mkdir.clear()
                    self.line_edit_mkdir.setText("Error in path!")

        else:
            if Window.iter_start == 0 and match != "admin":
                self.line_edit_mkdir.clear()
                self.line_edit_mkdir.setText("Permission denied!")

            elif text_mkdir not in lst_paths:
                try:
                    os.mkdir(text_mkdir)
                    self.line_edit_mkdir.clear()
                    self.line_edit_mkdir.setText("Ok!")
                    Window.update_paths(self)
                    
                except Exception as exc:
                    self.line_edit_mkdir.setText(f"{exc}")
                    Window.update_paths(self)

            else:
                self.line_edit_mkdir.clear()
                self.line_edit_mkdir.setText("Error in path!")


    def rmfile(self):
        global lst_files, index, start_time
        Window.update_paths(self)

        text_rmfile = lst_paths[index][:len_first_work_path + 1] + self.line_edit_rmfile.text()
        match = re.findall(r"You are (.{4,12}) \(", self.label_choose_role.text())[0]

        if time.time() - Window.start_time > 20:
            question = input(f"\n{dict_password_login[login][2]}\n")
            if question != dict_password_login[login][3]:
                sys.exit()
            else:
                Window.start_time = time.time()

                if Window.iter_start == 0 and match != "admin":
                    self.line_edit_rmfile.clear()
                    self.line_edit_rmfile.setText("Permission denied!")

                elif text_rmfile.split("/")[-1] in lst_files[index]:
                    try:
                        os.remove(text_rmfile)
                        self.line_edit_rmfile.clear()
                        self.line_edit_rmfile.setText("Ok!")
                        Window.update_paths(self)

                    except Exception as exc:
                        self.line_edit_rmfile.setText(f"{exc}")
                        Window.update_paths(self)

                else:
                    self.line_edit_rmfile.clear()
                    self.line_edit_rmfile.setText("Error in path!")
        else:
            if Window.iter_start == 0 and match != "admin":
                self.line_edit_rmfile.clear()
                self.line_edit_rmfile.setText("Permission denied!")

            elif text_rmfile.split("/")[-1] in lst_files[index]:
                try:
                    os.remove(text_rmfile)
                    self.line_edit_rmfile.clear()
                    self.line_edit_rmfile.setText("Ok!")
                    Window.update_paths(self)

                except Exception as exc:
                    self.line_edit_rmfile.setText(f"{exc}")
                    Window.update_paths(self)

            else:
                self.line_edit_rmfile.clear()
                self.line_edit_rmfile.setText("Error in path!")


    def rmdir(self):
        global lst_paths, start_time
        Window.update_paths(self)

        match = re.findall(r"You are (.{4,12}) \(", self.label_choose_role.text())[0]
        text_rmdir = lst_paths[index][:len_first_work_path + 1] + self.line_edit_rmdir.text()

        if time.time() - Window.start_time > 20:
            question = input(f"\n{dict_password_login[login][2]}\n")
            if question != dict_password_login[login][3]:
                sys.exit()
            else:
                Window.start_time = time.time()
                if Window.iter_start == 0 and match != "admin":
                    self.line_edit_rmdir.clear()
                    self.line_edit_rmdir.setText("Permission denied!")

                elif text_rmdir in lst_paths:
                    try:
                        shutil.rmtree(text_rmdir)
                        self.line_edit_rmdir.clear()
                        self.line_edit_rmdir.setText("Ok!")
                        Window.update_paths(self)
                    except Exception as exc:
                        self.line_edit_rmdir.setText(f"{exc}")
                        Window.update_paths(self)

                else:
                    self.line_edit_rmdir.clear()
                    self.line_edit_rmdir.setText("Error in path!")

        else:
            if Window.iter_start == 0 and match != "admin":
                self.line_edit_rmdir.clear()
                self.line_edit_rmdir.setText("Permission denied!")

            elif text_rmdir in lst_paths:
                try:
                    shutil.rmtree(text_rmdir)
                    self.line_edit_rmdir.clear()
                    self.line_edit_rmdir.setText("Ok!")
                    Window.update_paths(self)

                except Exception as exc:
                    self.line_edit_rmdir.setText(f"{exc}")
                    Window.update_paths(self)

            else:
                self.line_edit_rmdir.clear()
                self.line_edit_rmdir.setText("Error in path!")


    def vi(self):
        global lst_paths, lst_files, index, start_time
        Window.update_paths(self)
        match = re.findall(r"You are (.{4,12}) \(", self.label_choose_role.text())[0]
        name_file = lst_paths[index][:len_first_work_path + 1] + self.line_edit_vi.text()
        content_file = self.text_edit_vi.toPlainText()

        if time.time() - Window.start_time > 20:
            question = input(f"\n{dict_password_login[login][2]}\n")
            if question != dict_password_login[login][3]:
                sys.exit()
            else:
                Window.start_time = time.time()

                if Window.iter_start == 0 and match != "admin":
                    self.line_edit_vi.clear()
                    self.line_edit_vi.setText("Permission denied!")
                    self.text_edit_vi.clear()
                    self.text_edit_vi.insertPlainText("Permission denied!")

                elif name_file not in lst_files[index]:
                    os.chdir(lst_paths[index])
                    try:
                        with open(name_file, 'x') as f:
                            f.write(content_file)
                        self.line_edit_vi.clear()
                        self.line_edit_vi.setText("Ok!")
                        self.text_edit_vi.clear()
                        self.text_edit_vi.insertPlainText("Ok!")
                        Window.update_paths(self)
                    except Exception as exc:
                        self.line_edit_vi.clear()
                        self.line_edit_vi.setText(f"{exc}")
                        self.text_edit_vi.clear()
                        self.text_edit_vi.insertPlainText(f"{exc}")

                else:
                    self.line_edit_vi.clear()
                    self.line_edit_vi.setText("Error in path!")
                    self.text_edit_vi.clear()
                    self.text_edit_vi.insertPlainText("Error in path!")
        else:
            if Window.iter_start == 0 and match != "admin":
                self.line_edit_vi.clear()
                self.line_edit_vi.setText("Permission denied!")
                self.text_edit_vi.clear()
                self.text_edit_vi.insertPlainText("Permission denied!")

            elif name_file not in lst_files[index]:
                os.chdir(lst_paths[index])
                try:
                    with open(name_file, 'x') as f:
                        f.write(content_file)
                    self.line_edit_vi.clear()
                    self.line_edit_vi.setText("Ok!")
                    self.text_edit_vi.clear()
                    self.text_edit_vi.insertPlainText("Ok!")
                    Window.update_paths(self)
                except Exception as exc:
                    self.line_edit_vi.clear()
                    self.line_edit_vi.setText(f"{exc}")
                    self.text_edit_vi.clear()
                    self.text_edit_vi.insertPlainText(f"{exc}")

            else:
                self.line_edit_vi.clear()
                self.line_edit_vi.setText("Error in path!")
                self.text_edit_vi.clear()
                self.text_edit_vi.insertPlainText("Error in path!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
