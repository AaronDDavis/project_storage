# 📦 ProjectStorage - P2P Storage Marketplace

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Service%20Layer-orange?style=for-the-badge)
![Pattern](https://img.shields.io/badge/Pattern-Strategy%20%26%20Composite-blueviolet?style=for-the-badge)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://project-storage-app-ybvk.onrender.com/user/login)

> **Turning Shared Space into Shared Value**

**A decentralized “Uber-for-Storage” platform built with Django, featuring smart space allocation and OOD-driven architecture.**

---

## 📖 Table of Contents

- [✨ Overview](#-overview)
- [🚀 Live Demo](#-live-demo)
- [🖼️ Screenshots](#%EF%B8%8F-screenshots)
   - [🏠 Lessee Dashboard](#-lessee-dashboard)
   - [🔍 Lessee Search and Booking Flow](#-lessee-search-and-booking-flow)
   - [📊 Renter Space Detail & Visualization](#-renter-space-detail--visualization)
   - [👤 Admin Installation Request Detail Page](#-admin-installation-request-detail-page)
- [🚀 Version 5: The Engineering Refactor](#-version-5-the-engineering-refactor)
   - [🔍 Key Architectural Changes in v5](#-key-architectural-changes-in-v5)
- [🗓️ Changelog](#%EF%B8%8F-changelog)
- [⚙️ Core Features](#%EF%B8%8F-core-features)
- [📐 Allocation Strategy: Best-Fit with Compaction](#-allocation-strategy-best-fit-with-compaction)
- [🛠️ Tech Stack & Requirements](#%EF%B8%8F-tech-stack--requirements)
- [📁 Project Structure](#-project-structure)
- [💡 Core Engineering Rationale](#-core-engineering-rationale)
   - [High-Level Architecture: Service-Layer Pattern](#high-level-architecture-service-layer-pattern)
- [☁️ Deployment & DevOps](#%EF%B8%8F-deployment--devops)
- [💻 How to Run This Project Locally](#-how-to-run-this-project-locally)
   - [🧩 Test the Admin Verification Workflow](#-test-the-admin-verification-workflow)
- [🗺️ Future Development (Roadmap)](#%EF%B8%8F-future-development-roadmap)
- [🧾 License](#-license)
- [📬 Contact](#-contact)

---

## ✨ Overview

> **ProjectStorage** is a peer-to-peer storage marketplace that connects **Renters** (people with extra space) with **Lessees** (people who need to store items).

This repository contains **Version 5** of the application. This version represents a **major engineering refactor**, shifting the codebase from a "Fat Model/View" pattern toward a dedicated **Service-Layer Architecture** to ensure:

- **Separation of Concerns (SoC)**
- **High Testability**
- **Scalable Business Logic**

## 🚀 Live Demo

[![View Live Demo](https://img.shields.io/badge/🚀_Launch-Live_Demo-007bff?style=for-the-badge)](https://project-storage-app-ybvk.onrender.com/user/login)

> **Demo Credentials (Try it out):**
>
> - **Admin:** `admin` / `demo1234` *(View the verification queues)*
> - **Renter:** `renter` / `demo1234` *(View space visualization)*
> - **Lessee:** `lessee` / `demo1234` *(Test the booking algorithm)*

## 🖼️ Screenshots

### 🏠 Lessee Dashboard

![Lessee Dashboard Page](assets/lessee_dashboard.png)

### 🔍 Lessee Search and Booking Flow

![Search Space Page](assets/search_space_page.png)

![Booking Page](assets/booking_page.png)

### 📊 Renter Space Detail & Visualization

![Space Detail Page](assets/space_details_page.png)

*(Visualizes the **Space → Rack → Shelf Composite Pattern**)*

### 👤 Admin Installation Request Detail Page

![Admin Installation Request Detail Page](assets/admin_installation_request_detail.png)

<!--
> **[🎥 Watch the 1-Minute Evolution Video](#)** > *A walkthrough of how the architecture evolved from v1 to v5.*
-->

---

## 🚀 Version 5: The Engineering Refactor

Version 5 builds on existing features (Admin Verification, State Machines) by applying strict architectural patterns, centralizing domain logic, and eliminating business rules from controllers and data models.

### 🔍 Key Architectural Changes in v5

| Architectural Area | Previous Implementation | **New** v5 Implementation | Engineering Impact |
| :--- | :--- | :--- | :--- |
| **Business Logic** | Scattered between `views.py` and `models.py`. | Centralized in dedicated **Service Layers** (`services.py`, e.g., `InstallationRequestService`, `BookingStateService`). | Ensures **Separation of Concerns (SoC)** and to make it **Designed for Testability**. |
| **Error Handling** | Generic Django exceptions. | **Custom Exceptions** (`SpaceStateException`, `InstallationRequestError`) for precise control. | Provides **precise control** and clear, **domain-specific error semantics** for consumers. |
| **Domain Constants** | Hardcoded values within views/models. | **`constants.py`** (Centralized Configuration File). | Allows **easy modification** of pricing/locations without touching core logic (**Open/Closed Principle**). |
| **Data Modeling** | Single string field for location/address. | **New `Location` Model** with area codes and base prices. | Standardizes pricing logic and supports clearer **data integrity** for geographical definitions. |
| **Visualization** | Same logic embedded inside different views. | **`SpaceLayoutService`** (Visualization Logic separated from a particular view). | Adheres to **Single Responsibility Principle (SRP)** by not repeating presentation logic. |

## 🗓️ Changelog

- **v5 (Current):** Major Refactor to Service Layer & SOLID principles.
- **v4:** Added "Pre-listings" verification workflow.
- **v3:** Added Admin Dashboard.
- **v1-v2:** Prototype and core CRUD.

<details>
<summary>Click here to view the changelog in detail</summary>

### v5.0 (Current) - The Architecture Update

- **Service Layer Refactor:** Business logic moved strictly out of `views.py` / `models.py` into dedicated service modules (e.g., `InstallationRequestService`, `BookingFormService`).
- **Domain Constants:** `listings/constants.py` centralizes pricing, shelf dimensions, and location definitions.
- **Custom Exceptions:** Introduced a hierarchy of domain exceptions (e.g., `InstallationRequestError`, `BookingStatusException`) to decouple views from database integrity errors.
- **State Pattern Extension:** Extended the Finite State Machine pattern to the onboarding workflow via `InstallationRequestStateService`.
- **Allocation Strategy:** `BookingFormService` implements the **Best-Fit with compaction** allocation strategy for rack selection to reduce fragmentation.
- **Code Quality:** Extensive docstrings, comments, and type annotations added throughout the core modules.

### v4.0 - The "Prelistings" Workflow

- **New `Prelistings` App:** Introduced a dedicated workflow for onboarding new spaces to support physical verification.
- **Installation Request Model:** Renters now submit requests defining environmental conditions and location, rather than creating spaces directly.
- **Two-Phase Verification:** - Requests move through `PENDING` $\rightarrow$ `APPROVED` $\rightarrow$ `COMPLETED` lifecycles.
  - **Conversion Logic:** `InstallationRequestService.convert_to_space()` handles the atomic creation of Space, Racks, and Shelves only upon request completion.
- **Admin Queue:** Added a dedicated Admin Dashboard for reviewing Installation Requests before they become live Spaces.
- **UI/UX Enhancements:**
  - Renter dashboard separated into "My Requests" and "My Spaces".
  - Visual/UX consistency improvements using Bootstrap 5.

### v3.0 - The "Admin Verification" Workflow

- **Admin Verification Workflow:** Added a complete verification system.
  - New space statuses: `PENDING`, `APPROVED`, `REJECTED`, `ON_HOLD`.
  - New listings default to `PENDING` and are hidden from search.
  - Added an in-app Admin Dashboard for superusers to review, filter, approve, or reject listings.
  - Superusers are automatically redirected from the main dashboard to the Admin Verification Queue.
- **State Machine Refactor:**
  - Re-architected `Booking` and `Space` models to use `models.TextChoices` for managing statuses.
  - Enforced valid state transitions (e.g., an `APPROVED` space cannot revert to `PENDING`).
- **UI Enhancements:**
  - Renter dashboard now displays each listing’s verification status.
  - Admin dashboard is fully responsive (mobile + desktop).
  - Admin detail view reuses the Renter’s shelf visualization for review.
- **Superuser Workflow:** Automatic redirect to the Admin Queue on login.
- **Refactored Logic:** `update_space_status` now validates transitions and reduces conditional clutter.

### v2.0

- **Major architectural refactor** — introduced `Space → Rack → Shelf` hierarchy for more accurate spatial modeling.
- **State-driven Booking system** — bookings now managed via explicit lifecycle methods (`update_status`, `occupy_space`, `release_space`).
- **Improved user separation** — clearer role-based dashboards for Renters and Lessees.
- **Enhanced search & matching algorithm** — supports consecutive shelf detection and dynamic pricing.
- **Refined UI** — Bootstrap 5 layout cleanup and mobile-friendly booking flow.

</details>

---

## ⚙️ Core Features

### 🛡️ For Admins (Operational Workflow)

* **Two-Phase Verification:** Renters cannot create phantom spaces. They submit an `InstallationRequest`.
* **Admin Queue:** Superusers review requests, visualize the shelf layout, and "Install" the space digitally only after physical verification.
* **Automated Conversion:** Upon approval, the system atomically generates the `Space`, `Rack`, and `Shelf` database objects.

### 🏠 For Renters

* **Space Visualization:** A color-coded, grid-based view of their racks showing real-time occupancy.
* **Request Lifecycle:** Track status from `Pending` $\rightarrow$ `Approved` $\rightarrow$ `Live`.

### 🔍 For Lessees

* **Smart Search:** Filters spaces based on item dimensions (L x W x H) vs. available shelf configurations.
* **Dynamic Pricing:** Real-time cost calculation based on volume and duration.

<details>
<summary>Click here to view features in detail</summary>

### 👤 Dual User Roles & Account Management

- **Role-Based Access:** Users select a **Renter** or **Lessee** role upon sign-up, enabling distinct dashboard views and permissions.
- **Custom User Model:** Extends the built-in Django user for role-based permissions.

### 🛡️ Admin (Superuser) Features

- **Space Queue:** Admins are redirected to a dedicated dashboard that lists all `Spaces`, filterable by status (`Pending`, `Approved`, etc.)
- **Installation Request Queue:** Admins also have another dashboard that lists all `InstallationRequests`, filterable by status (`Pending`, `Approved`, etc.).
- **Lifecycle Management:** Admins control the transition of requests:
  1. **Approve:** Signals the Renter the location is valid.
  2. **Reject:** Denies the request.
  3. **Complete:** Confirms shelves are physically installed and triggers the **Space Conversion** logic.
- **Detailed Review:** Admins can edit shelf configurations (Rows × Columns) on the request before finalizing the Space.
- **Logic Enforcement:** The system prevents invalid transitions (e.g., cannot complete a request that hasn't been approved) via `StateServices`.

### 🏠 Renter Features

- **Installation Request Workflow:** Renters cannot create Spaces directly. Instead, they submit an **Installation Request**:
  - Selects a standardized **Location** (auto-populating base price from `constants.py`).
  - Defines **Environmental Conditions** and **Description**.
- **Request Management:** Renters can view the status of their requests (`Pending`, `Approved`, `Completed`) via the Dashboard.
- **Space Conversion:** Once a Request is marked `COMPLETED` (simulating physical shelf installation), the system converts it into a live **Space**, automatically generating the correct **Rack** and **Shelf** objects.
- **Space Detail & Visualization:** Allows Renters to see a visual, color-coded layout of their verified space, showing exactly which shelves are available and which are occupied.
- **Bookings per Space:** Renters can view all bookings (active, upcoming and past) associated with a specific Space.

### 🔍 Lessee Features & Smart Booking

- **Smart Search:** Search is based on **location** and the **dimensions** of the package (Length × Width × Height).
- **Smart Filtering Algorithm:**
  - Calculates the number of shelves required based on the item's length.
  - Finds spaces that contain at least one Rack long enough for the item and with enough **consecutively available shelves**.
- **Efficient Booking:** The system automatically assigns a new booking to the **most appropriate Rack** to optimize space usage.
- **Algorithmic Allocation (Best-Fit Strategy):** `BookingFormService` automatically selects the most suitable Rack to minimize fragmentation and optimize usage.
- **Dynamic Price Calculation:** Includes a dynamic calculator that updates the total price instantly based on the number of days and shelves selected.
- **Booking History:** Dashboard shows a clear view of active and past bookings.
- **State-Separated Dashboard:** Active and upcoming bookings are displayed separately from past and cancelled ones for clarity.
- **Booking Details:** Lessees can view a dedicated summary page for each booking, showing its status, duration, and cost.
- **Booking Cancellation:** Lessees can cancel their future bookings via a secure, mobile-friendly modal.

</details>

---

## 📐 Allocation Strategy: Best-Fit with Compaction

The platform uses the **Best-Fit with Compaction** strategy to manage space efficiently, aiming to prevent the fragmentation of large storage areas into small, unusable chunks. This logic is strictly centralized in the `BookingFormService` via an ORM-based implementation of the Strategy Pattern.

<details>
<summary>
<h3 style='display: inline-block'> 🧠 Algorithmic Flow </h3>
</summary>

1. **Quantify Potential:** The system first queries all racks in the selected space, annotating each one with the **total count of its currently available shelves**.
2. **Filter by Need:** It then immediately filters this list to exclude any rack whose **total available shelf count** is less than the number of contiguous shelves required by the Lessee.
3. **Best-Fit Selection:** The remaining suitable racks are sorted in **ascending order** based on their total available shelf count.
4. **Compaction Goal:** By selecting the first rack in this sorted list (`.order_by('available_shelves').first()`), the system ensures the new booking is placed in the rack that leaves the **smallest excess capacity** remaining. This compacts the open space, leaving larger, more useful continuous blocks available in other racks.

> **Note on Contiguity:** The query logic ensures the selected rack has the *capacity* for the booking; the subsequent domain logic then handles the final verification and marking of the specific **consecutive shelf block** within that chosen rack.

</details>

---

## 🛠️ Tech Stack & Requirements

| Component | Technology | Version | Description |
| :--- | :--- | :--- | :---|
| **Backend** | Python & Django | Python 3, Django 5.x | Robust and secure web framework for rapid development. |
| **Frontend** | Django Templates (HTML), Bootstrap, JS | Bootstrap 5, Vanilla JavaScript | Responsive design with minimal client-side complexity. |
| **Database** | PostgreSQL | 14+ | Production Database |
| **Server** | Gunicorn | 23.x | Production-grade WSGI HTTP Server |
| **Static Files** | WhiteNoise | 6.x | Efficient static file serving for production |
| **Infrastructure** | Render (PaaS) | - | Cloud hosting and continuous deployment pipeline |
| **Architecture** | Service-Oriented | - | MVT + Service Layer Pattern. |

---

## 📁 Project Structure

The project is organized into cohesive apps, each following a strict internal layering:

- **/users:** Authentication, Registration, User Profiles.
- **/prelistings:** (New)
  - `models.py`: `InstallationRequest`.
  - `services.py`: `InstallationRequestService` (Conversion logic), `InstallationRequestStateService` (Transitions).
  - `exceptions.py`: Custom `InstallationRequestError`.
- **/listings:**
  - `models.py`: `Space`, `Rack`, `Shelf`, `Location`.
  - `services.py`: `SpaceService` (CRUD), `SpaceStateService` (Transitions), `SpaceLayoutService` (Visualization).
  - `constants.py`: Location definitions and shelf dimensions.
  - `exceptions.py`: Custom `SpaceStateException`.
- **/bookings:**
  - `models.py`: `Booking`.
  - `services.py`: `BookingService` (Calculations), `BookingStateService` (Lifecycle), `BookingFormService` (Allocation).
  - `exceptions.py`: Custom `BookingStatusException`.

---

## 💡 Core Engineering Rationale

This project leverages several key **software design principles** and **patterns** to create a scalable, maintainable, and robust system.

> **📄 Read the full Architectural Breakdown: [SOFTWARE_DESIGN.md](SOFTWARE_DESIGN.md) file.**

### High-Level Architecture: Service-Layer Pattern

Version 5 moves the codebase toward a **Service-Oriented Architecture**:

- **Views (`views.py`)** — handle HTTP, permissions, and input parsing. They delegate business logic to Services.
- **Services (`services.py`)** — framework-agnostic classes that implement business logic (calculations, allocation, transitions). Services are easy to unit test and reuse (CLI, API, background jobs).
- **Models (`models.py`)** — strictly define data schema and relationships (no business logic).

---

<details>
<summary>
<h3 style='display: inline-block'> 🛡️ S.O.L.I.D. Principles Applied </h3>
</summary>

| Principle | How It Is Applied in ProjectStorage |
| --- | --- |
| **S — Single Responsibility** | Each artifact has one responsibility: Views handle HTTP; Services contain business logic (e.g., `BookingService` for calculations, `BookingStateService` for lifecycle rules); Models define schema/state only. For example, pricing logic can change in `BookingService` without modifying `models.py`. |
| **O — Open/Closed** | Behavior is extended via configuration and subclassing rather than modifying core logic. Examples: Django CBV hooks (`get_queryset()`), and domain constants in `listings/constants.py` allow adding new pricing or location logic without modifying service internals. |
| **L — Liskov Substitution** | Custom domain types preserve their parent contracts. Example: `CustomUser` inherits `AbstractUser` and remains compatible everywhere Django expects a user object. |
| **I — Interface Segregation** | Behavior is composed through small Mixins (e.g., `LoginRequiredMixin`, `UserPassesTestMixin`) rather than large base classes, ensuring class interfaces remain minimal. |
| **D — Dependency Inversion** | Business logic depends on abstractions (enums, services) rather than raw literals or infrastructure details. For example, `Booking.status` uses `models.TextChoices`, so callers depend on `Booking.Status.*` instead of string values. Allocation strategy objects can be injected into services. |

</details>

---

<details>
<summary>
<h3 style='display: inline-block'> 🧱 Key Design Patterns Implemented </h3>
</summary>

| Pattern | Where | Rationale | Example |
| --- | --- | --- | --- |
| **Service Layer Pattern** | `services.py` | Decouples business logic from Django framework concerns, improving testability and reuse. | `SpaceService.create_shelves(...)` encapsulates shelf generation for views, scripts, and tests. |
| **State Pattern (Finite State Machine)** | State Services (e.g., `BookingStateService`, `SpaceStateService`) | Enforces valid lifecycle transitions and ensures consistent triggering of side effects. | `BookingStateService.update_status()` triggers `occupy_space`/`release_space` upon transition. |
| **Strategy Pattern** | `BookingFormService.get_rack` | Enables swapping allocation algorithms (Best-Fit, First-Fit, Load-Balancing) without altering booking workflows. | Current strategy: Best-Fit with Compaction. |
| **Facade Pattern** | `SpaceService.get_available_spaces` | Simplifies complex ORM queries and prefetch behavior behind a clean API. | Views call a single service method rather than constructing complex annotated queries. |
| **Composite Pattern** | `listings/models.py` (`Space → Rack → Shelf`) | Models a hierarchical structure as a single aggregate for querying and visualization. | Enables aggregate queries (e.g., `space.total_shelves`) and shelf-level availability rendering. |
| **Repository Pattern (Service-as-Repository style)** | Query helpers in services | Centralizes query building for consistency and reuse. | `SpaceService.get_spaces(...)` instead of inline `Space.objects.filter(...)` in views. |

</details>

---

## ☁️ Deployment & DevOps

The application is deployed on **Render** using a continuous deployment pipeline. The setup follows **Twelve-Factor App** methodologies to ensure security and reproducibility:

- **Infrastructure as Code:** Deployment logic is version-controlled via `build.sh`, which automates dependency installation, static file collection, and migrations.
- **Process Management:** A `Procfile` declares the application's entry point, instructing the cloud provider to serve the app using **Gunicorn** rather than the development server.
- **Automated Provisioning:** A custom script (`scripts/create_superuser.py`) runs during the build process to auto-provision administrative access, bypassing the need for interactive SSH consoles.
- **Environment Security:** `SECRET_KEY`, `DEBUG`, and Database credentials are strictly decoupled from the codebase and managed via environment variables (`os.environ`).
- **Database Switching:** The system uses `dj-database-url` to automatically detect the environment and switch between **SQLite** (local) and **PostgreSQL** (production).

---

## 💻 How to Run This Project Locally

1. **Clone the repository:**

    ```sh
    git clone https://github.com/AaronDDavis/project_storage.git
    cd project_storage
    ```

2. **Create and activate a virtual environment:**

    ```sh
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```sh
    # Installs production + dev requirements
    pip install -r requirements.txt
    ```

4. **Environment Setup:**

   Create a `.env` file in the root directory (or export these variables in your terminal) to mimic production security:

   ```env
   DEBUG=True
   SECRET_KEY=your-local-secret-key
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Run database migrations:**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

    *Allows you to access the `/admin` panel.*

7. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

8. Open your browser and go to `http://127.0.0.1:8000/user/signup`.

---

### 🧩 Test the Admin Verification Workflow

1. **Create accounts:**
   - Sign up as a **Renter** and create a new Request.
   - Log out and log in as a **Superuser**.
2. **Review queue:**  
   Superusers are redirected automatically to the **Admin Verification Queue** (`/admin/space/list/`).
   - Proceed to requests tab
3. **Approve or reject:**  
   - Review the new request, and approve/reject accordingly.
   - Add number of racks and shelves and mark as completed
4. **Convert to Space:**
   - Login as the Renter, and convert the completed request to a space
5. **Verify visibility:**  
   - Log in as a **Lessee** — the listing will be visible in the search view.

---

## 🗺️ Future Development (Roadmap)

- **💸 Payment Integration:** Integrate Stripe or a similar service to handle secure real-time payments.
- **💬 Chat/Messaging System:** Allow Lessees and Renters to communicate directly within the platform.
- **Image Upload:** Allow Renters to upload images of their space during space creation.

---

## 🧾 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You’re welcome to use, modify, or build upon this project for learning or non-commercial purposes.

---

## 📬 Contact

Developed by **Aaron Davis**

Email: [aaronddavis001@gmail.com]

LinkedIn: [https://linkedin.com/in/aaron-daniel-davis]
