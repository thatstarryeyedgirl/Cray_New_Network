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
| POST | `/api/register/` | Create a new editor account |
| POST | `/api/login/` | Log in as a Chief Editor |
| POST | `/api/forgot-password/` | Send password reset link |
| POST | `/api/reset-password/<uidb64>/<token>/` | Reset password using token |

### 2. News Management  
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | `/news/create/` | Create a new news article |
| PUT | `/news/edit/<int:id>/` | Edit an existing article |
| DELETE | `/news/delete/<int:id>/` | Delete a news article |
| GET | `/news/all/` | Retrieve all published news |
| GET | `/news/search/?title=keyword` | Search for news by title |

### 3. Users


## Tech Stack  
- **Backend Framework:** Django & Django REST Framework (DRF)  
- **Database:** PostgreSQL  
- **Language:** Python 3.12.10  
- **Authentication:** JWT (JSON Web Token)  
- **Environment Management:** `.env`

## Postman Documentation  
The **Cray New Network API** is fully documented in Postman for easy testing and endpoint validation.  
The collection includes requests for authentication, news management, and content search — with preconfigured methods, headers, and example payloads.  

- **Postman Link:** ``


