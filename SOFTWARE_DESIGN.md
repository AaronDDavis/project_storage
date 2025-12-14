# 📐 Software Design & Architecture

> This document outlines the engineering decisions, architectural patterns, and SOLID principles applied in **ProjectStorage (v5)**.

---

## 🏗️ High-Level Architecture: Service-Layer Pattern

In Version 4, the application moved from a standard "Django MVT" (Model-View-Template) pattern to a **Service-Oriented Architecture**.

### The Problem *(version 4)*

In previous versions, business logic (e.g., calculating prices, validating state transitions, finding the best rack) was placed inside **Views** or **Models**. This led to:

1. **"Fat Models":** Models became bloated with non-database logic.
2. **Untestable Views:** Testing business logic would require simulating entire HTTP requests.
3. **Low Reusability:** Logic written in a View couldn't be reused in another View or API.

### The Solution *(version 5)*

Introduced a **Service Layer** (`services.py` in each app).

* **Views (`views.py`)**: Handle HTTP requests, permissions, and form parsing. They **delegate** all heavy lifting to Services.
* **Services (`services.py`)**: Pure Python classes that contain the **Business Logic**. They are framework-agnostic where possible.
* **Models (`models.py`)**: Strictly define the **Data Schema** and relationships.

---

## 🛡️ S.O.L.I.D. Principles

### **S - Single Responsibility Principle (SRP)**

* **Service Extraction:**
  * **File:** `bookings/services.py`
  * **Concept:** The `Booking` model (in `models.py`) strictly holds data (State). The `BookingService` holds calculation logic (Behavior). The `BookingStateService` holds transition logic (Lifecycle).
  * **Impact:** If we need to change how prices are calculated, we touch `BookingService`. If we need to change database fields, we touch `models.py`. This separation reduces the risk of regression bugs.

* **View Delegation:**
  * **File:** `listings/views.py` (`SpaceListView`)
  * **Concept:** The view does not know *how* to filter spaces by dimension or location. It simply delegates to `SpaceService.get_available_spaces(...)`.
  * **Impact:** The View has one responsibility: **HTTP Protocol handling** (receiving parameters and rendering a template).

### **O - Open/Closed Principle (OCP)**

* **Django Class-Based Views (CBVs):**
  * **File:** `listings/views.py`
  * **Concept:** We extend Django's `CreateView` and `ListView`. We do not modify Django's source code; instead, we extend functionality by overriding "hooks" like `get_queryset()` and `get_context_data()`.

* **Configuration Constants:**
  * **File:** `listings/constants.py`
  * **Concept:** Pricing logic and Location definitions are extracted into a constants file (`LOCATION_DEFS`).
  * **Impact:** We can add new locations or change base prices (Extension) without modifying the calculation logic in `SpaceService` (Closed for modification).

### **L - Liskov Substitution Principle (LSP)**

* **Custom User Model:**
  * **File:** `users/models.py`
  * **Concept:** `CustomUser` inherits from `AbstractUser`.
  * **Impact:** `CustomUser` can be substituted anywhere Django expects a user object (e.g., `request.user`, `ForeignKey`). It fulfills the contract of the parent class while adding domain-specific fields (`role`, `nric_fin`).

### **I - Interface Segregation Principle (ISP)**

* **Mixin Composition:**
  * **File:** `listings/views.py`
  * **Concept:** `SpaceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView)`
  * **Impact:** Instead of inheriting from one massive "SuperView" that does everything, the class composes its behavior from small, specific interfaces (Mixins). It only "imports" the functionality it explicitly needs.

### **D - Dependency Inversion Principle (DIP)**

* **Abstractions over Concretions:**
  * **File:** `bookings/models.py`
  * **Concept:** `Booking.status` uses `models.TextChoices` (`Booking.Status`).
  * **Impact:** The business logic depends on the abstract Enum members (e.g., `Booking.Status.ACTIVE`), not on the "magic strings" ('ACTIVE') stored in the database.

* **Abstractions in Error Types:**
  * **File:** `prelistings/exceptions.py`
  * **Classes:** `InstallationRequestError` (Base), `InstallationRequestConversionError` (Specific)
  * **Justification:** The application code depends on **abstract error types** (`InstallationRequestConversionError`) rather than checking raw transition logic strings. This ensures high-level modules only rely on the specified interface of the error hierarchy, inverting the dependency from concrete status checks to abstract error contracts.

---

## 🧱 Design Patterns Implemented

### 1. State Pattern (State Machine)

**Context:** The application manages two separate, critical lifecycles: booking fulfillment and listing installation.

* **Implementation 1: Bookings**
  * **File:** `bookings/services.py`
  * **Class:** `BookingStateService`
  * **Explanation:** Manages the lifecycle from `BOOKED` to `ACTIVE` to `PAST`.

* **Implementation 2: Prelistings**
  * **File:** `prelistings/services.py`
  * **Class:** `InstallationRequestStateService`
  * **Explanation:** Manages the lifecycle from `PENDING` $\to$ `APPROVED` $\to$ `COMPLETED`. The `COMPLETED` state is the only valid trigger for the **Builder Pattern** (conversion to a live `Space`).

### 2. Strategy Pattern

**Context:** When a user books a space, the system must decide *which* Rack to assign them to.

* **Implementation:** `bookings/services.py` -> `BookingFormService.get_rack`.
* **Detail:** The current strategy is **"Best Fit with Compaction"** (find the rack with the *fewest* available shelves that still fits the item).
* **Why it matters:** If we want to change this later to a "First Fit" or "Load Balancing" strategy, we only change the algorithm in this service method without breaking the Booking View.

### 3. Facade Pattern

**Context:** Filtering spaces by dimensions involves complex join operations, subqueries, and annotations (`Count`, `Subquery`, `OuterRef`).

* **Implementation:** `listings/services.py` -> `SpaceService.get_available_spaces`.
* **Detail:** This static method acts as a **Facade**. The View calls one simple line of code. Behind the scenes, the Facade orchestrates a complex `QuerySet` construction involving checking `Status.APPROVED`, filtering by shelf dimensions, and calculating contiguous availability.

### 4. Composite Pattern

**Context:** A Storage Space is made of Racks, and Racks are made of Shelves.

* **Implementation:** `listings/models.py` (`Space` → `Rack` → `Shelf`).
* **Detail:** This hierarchy allows us to treat a "Space" as a single object while it is actually a composition of many parts. This enables powerful aggregate queries, such as `space.total_shelves` (which calculates the sum of all shelves in all racks recursively).

### 5. Repository Pattern (Subset)

**Context:** Views often repeat filter logic

* **Implementation 1:** `listings/services.py` -> `SpaceService.get_spaces`
* **Implementation 2:** `prelistings/services.py` -> `InstallationRequestService.get_installation_requests`
* **Detail:** These service methods centralize query logic. Views call `get_installation_requests(renter=user)` instead of writing raw ORM filters like `InstallationRequest.objects.filter(renter=user)`.

### 6. Decorator Pattern

**Context:** Used to **modify the behavior of a function or method without changing its source code**. It's applied extensively in Python and Django for cross-cutting concerns like security and HTTP method enforcement.

* **Implementation:** `listings/views.py`, -> `@login_required`, `@require_POST`;`listings/services.py` -> `@staticmethod`
* **Detail:**
  * In views, `@require_POST` (e.g., on `update_space_status`) enforces **HTTP standards**, automatically rejecting non-POST requests.
  * In Services, `@staticmethod` is used for methods that are logically related to the class (e.g., helper functions) but **do not require or modify the class's state**, promoting **functional purity**.

### 7. Builder Pattern

**Context:** The creation of a live `Space` listing is a complex, multi-step process involving the construction of a hierarchical data structure (`Location` $\to$ `Space` $\to$ `Rack` $\to$ `Shelf`). The Builder pattern manages this complexity.

* **Implementation:** `prelistings/services.py` -> `InstallationRequestService.convert_to_space`
* **Detail:** This method acts as the **Director/Builder**. It takes the simple, validated `InstallationRequest` object and systematically orchestrates the creation of the full composite asset (`Space`, `Racks`, `Shelves`) before deleting the temporary request. This ensures the final **complex object is valid, complete, and correctly initialized.**

---

## Practical Engineering Benefits

* **Testability:** Business rules live in Services, allowing pure unit tests without HTTP or full DB fixtures (where appropriate).
* **Reusability:** Services can be reused across HTTP views, CLI commands, and background jobs.
* **Maintainability:** Transitions and side effects are centralized in `*StateService` classes rather than spread across many views.
* **Extensibility:** Updating pricing rules, allocation algorithms, or lifecycle logic typically requires modifying only one service or constants file.
