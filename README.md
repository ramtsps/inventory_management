# Inventory Management System

This is a web-based inventory management system developed using Django.

## Features

- Add/edit/delete products
- Track stock levels
- Generate reports
- User authentication

## Project Flow

```mermaid
flowchart TD
    A[Login] --> B[Dashboard]
    B --> C[Add Product]
    B --> D[View Inventory]
    D --> E{Stock Available?}
    E -->|Yes| F[Order Processed]
    E -->|No| G[Notify Admin]
```
