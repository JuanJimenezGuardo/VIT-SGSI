# API Validation Day 5

Fecha: 2026-03-18
Responsable: Juan Jose Jimenez Guardo
Sprint: 2

## Alcance validado

- contacts
- project-contacts
- documents

## Evidencia de ejecucion

Comando ejecutado:

python manage.py test apps.contacts.tests.test_api apps.projects.tests.test_api.ProjectContactAPITest apps.documents.tests.test_api --verbosity 2

Resultado:

- 16 tests ejecutados
- 16 tests OK
- Sin errores

## Checklist QA manual

### Contacts

- GET: OK (200)
  - test_list_contacts_api
- POST: OK (201)
  - test_create_contact_via_api
- PATCH: OK (200)
  - test_update_contact_work_notes_api
- Validacion 400: OK (400)
  - test_create_contact_duplicate_email_returns_400

### ProjectContacts

- GET: OK (200)
  - test_list_project_contacts
- POST: OK (201)
  - test_create_project_contact
- PATCH: OK (200)
  - test_patch_project_contact
- Validacion 400: OK (400)
  - test_create_project_contact_cross_company_returns_400

### Documents

- GET: OK (200)
  - test_list_documents_api
- POST: OK (201)
  - test_create_document_with_dates
- PATCH: OK (200)
  - test_update_document_dates_api
- Validacion 400: OK (400)
  - test_create_approved_document_without_approver_returns_400

## Ajustes aplicados para estabilidad de validaciones 400

- Contact serializer: validator de unicidad company + email
- ProjectContact serializer: conversion de ValidationError de modelo a respuesta DRF 400
- Document serializer: conversion de ValidationError de modelo a respuesta DRF 400

## Conclusion

La API cumple el checklist solicitado para los tres modulos: GET, POST, PATCH y validacion 400.
