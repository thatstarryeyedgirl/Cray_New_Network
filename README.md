# Cray_New_Network

Welcome to **Cray New Network (CNN)**!  
This project is a **Django RESTful API** built to redefine the news experience for a new generation of readers.  
It focuses on creating a dynamic, millennial-friendly platform where editors can manage content seamlessly and users can easily explore the latest stories.

## Overview

The **Cray New Network API** serves as the backend for a modern news platform reimagined for the digital age.  
It provides secure authentication for **Chief Editors**, allowing them to:
- Create an account and log in securely.  
- Post new news articles with **text, images, or videos**.  
- Edit or delete existing articles (for corrections, plagiarism, or political reasons).  
- Reset forgotten passwords and recover accounts easily.

**Users** can:  
- View all available news.  
- Search for specific stories by title.
This backend is designed to integrate smoothly with the frontend, ensuring fast performance and scalability.

### 1. Authentication  
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | `/auth/signup/` | Create a new editor account |
| POST | `/auth/login/` | Log in as a Chief Editor |
| POST | `/auth/forgot-password/` | Send password reset link or code |
| POST | `/auth/reset-password/` | Reset password using token or code |

