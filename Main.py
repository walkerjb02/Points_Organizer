import tkinter as tk
from form import createform,add_email
from PIL import ImageTk, Image
import json
import webbrowser as wb
from form import drive_service
from startup import add_to_startup, remove_from_startup,get_MAC

def GUI():
    get_MAC()
    root = tk.Tk()
    root.title('PointsOrganizer')
    coolgrey = '#464a4f'
    canvas1 = tk.Canvas(root, width=175, height=400, bg='#006df2', relief='groove',
                        bd=10)
    canvas1.pack()
    image = r'C:\Users\gsbaw\PycharmProjects\PointsOrganizer\background.png'#TODO FIX FILEPATH
    img = ImageTk.PhotoImage(Image.open(image))
    panel = tk.Label(root, image=img)
    panel.place(x=0, y=0)
    button1 = tk.Button(text='Make a New Form', command=formcreatewindow, bg='#464a4f', fg='white', width=20,
                        height=10, border=5, font=('Aharoni', 8, 'bold'))
    canvas1.create_window(100, 100, window=button1)

    button1 = tk.Button(text='Settings', command=settings, bg=coolgrey, fg='white', width=20, height=10, border=5,
                        font=('Aharoni', 8, 'bold'))
    canvas1.create_window(100, 300, window=button1)

    filemenu = tk.Menu(tk.Menu(), tearoff=10)
    filemenu.add_command(label="Points Organizer", command=None, font=('Aharoni', 90, 'bold'))
    filemenu.add_separator()
    root.config(menu=filemenu)
    root.mainloop()


def formcreatewindow():
    def add_to_form():
        with open('Storage.json','r+') as file:
            jon = json.load(file)
            with open('FormStorage1.json', 'r+') as file:
                new = json.load(file)
                fileID = createform(entry1.get(), description.get())
                new["files"][0][f"{entry1.get()}"] = f"{fileID}"
                new = json.dumps(new)
                with open('FormStorage1.json', 'w') as nfile:
                    nfile.write(new)
                    batch = drive_service.new_batch_http_request()
                    user_permission = {
                        "type": "user",
                        "role": "writer",
                        "emailAddress": f"""{jon["emails"][0]}""",
                    }
                    batch.add(drive_service.permissions().create(
                        fileId=f"{fileID}",
                        body=user_permission,
                        fields="id",
                        sendNotificationEmail=True))
                    batch.execute()
                wb.open(f'https://docs.google.com/forms/d/{fileID}')
    root = tk.Toplevel()
    root.title("PointsOrganizer Form Creator")
    canvas2 = tk.Canvas(root, width=160, height=200, bg='#006df2', relief='groove',bd=10)
    canvas2.pack()
    path = r'C:\Users\gsbaw\PycharmProjects\PointsOrganizer\background.png' #TODO FIX FILEPATH
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(root, image=img)
    panel.photo = img
    panel.place(x=00, y=00)
    rootmenu = tk.Menu(root, tearoff=10)
    rootmenu.add_command(label="Form Creator", command=None, font=('Aharoni', 90, 'bold'))

    label1 = tk.Label(root, text="Both Fields Required", bg='#464a4f', fg='white', font=('Aharoni', 8, 'bold'),width=20)
    canvas2.create_window(90, 20, window=label1)

    label1 = tk.Label(root,text="Document Title", bg='#464a4f', fg='white', font=('Aharoni', 8, 'bold'),width=21)
    canvas2.create_window(90,55,window=label1)
    entry1 = tk.Entry(root,width=24)
    canvas2.create_window(90, 80, window=entry1)

    label2 = tk.Label(root, text="Form Title", bg='#464a4f', fg='white', font=('Aharoni', 8, 'bold'),width=21)
    canvas2.create_window(90, 115, window=label2)
    description = tk.Entry(root, width=24)
    canvas2.create_window(90, 140, window=description)
    label1 = tk.Button(root, text="Create Form", command=add_to_form, bg='#464a4f', fg='white', font=('Aharoni', 8, 'bold'))
    canvas2.create_window(90, 170, window=label1)
    rootmenu.add_separator()
    root.config(menu=rootmenu)


def settings():
    def emailpermissionadd():
        mail = emailz.get()
        with open('Storage.json','r+') as file:
            jon = json.load(file)
            if len(jon["emails"]) > 0:
                jon["emails"].pop()
            else:pass
            jon["emails"].append(f"{mail}")
            new = json.dumps(jon)
            with open('Storage.json', 'w') as nfile:
                nfile.write(new)
            add_email()


    def add_category():
        npcat = pcat.get()
        nptot = ptot.get()
        with open('Pointtotals.json','r+') as file:
            jon = json.load(file)
            jon["pointtotals"].append({f"{npcat}":[f"{nptot}",{}]})
            new = json.dumps(jon)
            with open('Pointtotals.json', 'w') as nfile:
                nfile.write(new)


    root = tk.Toplevel()
    root.title("PointsOrganizer Settings")
    rootmenu = tk.Menu(root, tearoff=10)
    rootmenu.add_command(label="Settings", command=None, font=('Aharoni', 90, 'bold'))
    rootmenu.add_separator()
    root.config(menu=rootmenu)
    canvas2 = tk.Canvas(root, width=200, height=370, bg='#006df2', relief='groove', bd=10)
    path = r'C:\Users\gsbaw\PycharmProjects\PointsOrganizer\background.png'#TODO FIX FILEPATH
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(root, image=img)
    panel.photo = img
    panel.place(x=00, y=00)
    canvas2.pack()

    label2 = tk.Label(root, text="Email Address to Link", bg='#464a4f', fg='white', font=('Aharoni', 8, 'bold'), width=20)
    canvas2.create_window(112, 40, window=label2)
    emailz = tk.Entry(root, width=20)
    canvas2.create_window(110, 70, window=emailz)
    label1 = tk.Button(root, text="Link Email", command=emailpermissionadd, bg='#464a4f', fg='white',
                       font=('Aharoni', 8, 'bold'), width=20)
    canvas2.create_window(112, 100, window=label1)


    label1 = tk.Button(root, text="Enable Updates on Statup", command=add_to_startup, bg='#464a4f', fg='white',
                       font=('Aharoni', 8, 'bold'), width=20)
    canvas2.create_window(112, 150, window=label1)

    label1 = tk.Button(root, text="Disable Updates on Statup", command=remove_from_startup, bg='#464a4f', fg='white',
                       font=('Aharoni', 8, 'bold'), width=20)
    canvas2.create_window(112, 180, window=label1)


    label2 = tk.Label(root, text="Add Point Category", bg='#464a4f', fg='white', font=('Aharoni', 8, 'bold'),
                      width=20)
    canvas2.create_window(112, 230, window=label2)
    pcat = tk.Entry(root, width=20)
    canvas2.create_window(110, 260, window=pcat)

    label2 = tk.Label(root, text="Add Number Required", bg='#464a4f', fg='white', font=('Aharoni', 8, 'bold'),
                      width=20)
    canvas2.create_window(112, 290, window=label2)

    ptot = tk.Entry(root, width=20)
    canvas2.create_window(110, 320, window=ptot)
    label1 = tk.Button(root, text="Append Category", command=add_category, bg='#464a4f', fg='white',
                       font=('Aharoni', 8, 'bold'), width=20)
    canvas2.create_window(112, 350, window=label1)

GUI()
