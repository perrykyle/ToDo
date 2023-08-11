# ToDo Project: Manage Your Weekly Tasks (Source Code)

![Project Banner](ToDo(v3)\resources\todo.PNG)


> **Note**: This is the source code to the project. The full project implementation and release are in the "Release" branch

## Table of Contents
- [Current Features](#current-features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [License](#license)

## Current Features
- **ToDo Manager GUI**: Add, view, and delete your weekly tasks, as well as view and delete your upcoming non-weekly tasks
- **Authentication**: Easily authenticate yourself with the Graph API within the GUI, and refresh your access token when needed
- **Microsoft Graph ToDo Integration**: Weekly tasks that are added to the GUI are automatically added to Microsoft ToDo
- **Apple Reminders Integration**: Signing into your Microsoft account within apple reminders will automatically add your reminders to Microsoft ToDo, and format them appropriately to fit in with your weekly tasks
- **Refresh your tasks on command**: Refresh your tasks on command to ensure that your tasks are up-to-date in your GUI and the Microsoft ToDo application

![Current Feature Image](ToDo(v3)/resources/auth.png)

## Technologies Used
- Microsoft Graph API
- Microsoft ToDo
- tkinter
- Express
- PyInstaller

## Setup and Installation
The current working version is in [ToDo(v3)](ToDo(v3)), if you're looking to install, the best version to use is in the Release branch.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
