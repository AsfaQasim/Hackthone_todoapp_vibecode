# CLI Interface Contract: Phase I In-Memory CLI Todo App

**Date**: 2026-01-02
**Feature**: Phase I In-Memory CLI Todo App
**Purpose**: Define CLI menu structure, commands, input/output formats, and error messages

## Interface Type

**Pattern**: Menu-driven interactive CLI
**Input Method**: Standard input (stdin) with numbered menu options
**Output Method**: Standard output (stdout) with formatted text

## Menu Structure

### Main Menu

```
=== Todo CLI ===
1. Add Todo
2. View All Todos
3. Filter Todos
4. Mark Todo Complete
5. Mark Todo Incomplete
6. Update Todo
7. Delete Todo
8. Exit

Enter your choice (1-8):
```

### Filter Submenu

```
=== Filter Todos ===
1. Show All
2. Show Complete Only
3. Show Incomplete Only
4. Back to Main Menu

Enter your choice (1-4):
```

## Command Specifications

### 1. Add Todo

**Menu Option**: 1
**User Input Required**: Description (string)

**Input Prompt**:
```
Enter todo description: _
```

**Success Output**:
```
✓ Todo added successfully!
  ID: 1
  Description: Buy groceries
  Status: Incomplete
```

**Error Scenarios**:

| Error Condition         | User Message                                          |
|-------------------------|-------------------------------------------------------|
| Empty description       | "✗ Error: Description cannot be empty."               |
| Whitespace only         | "✗ Error: Description cannot be empty."               |
| Too long (>500 chars)   | "✗ Error: Description cannot exceed 500 characters."  |

---

### 2. View All Todos

**Menu Option**: 2
**User Input Required**: None

**Output Format** (with todos):
```
=== All Todos ===

ID | Status      | Description
---|-------------|------------------------------------------
1  | Incomplete  | Buy groceries
2  | Complete    | Finish homework
3  | Incomplete  | Read Clean Code book

Total: 3 todos (1 complete, 2 incomplete)
```

**Output Format** (no todos):
```
=== All Todos ===

No todos found. Use option 1 to add your first todo!
```

**Error Scenarios**: None (always succeeds)

---

### 3. Filter Todos

**Menu Option**: 3
**User Input Required**: Filter choice (1-4 from submenu)

**Submenu Display**: See "Filter Submenu" above

**Output Format** (show complete):
```
=== Completed Todos ===

ID | Status    | Description
---|-----------|------------------------------------------
2  | Complete  | Finish homework

Total: 1 complete todo
```

**Output Format** (show incomplete):
```
=== Incomplete Todos ===

ID | Status      | Description
---|-------------|------------------------------------------
1  | Incomplete  | Buy groceries
3  | Incomplete  | Read Clean Code book

Total: 2 incomplete todos
```

**Output Format** (no matches):
```
=== [Complete/Incomplete] Todos ===

No [complete/incomplete] todos found.
```

**Error Scenarios**:

| Error Condition         | User Message                                 |
|-------------------------|----------------------------------------------|
| Invalid menu choice     | "✗ Error: Please enter a number between 1-4."|

---

### 4. Mark Todo Complete

**Menu Option**: 4
**User Input Required**: Todo ID (integer)

**Input Prompt**:
```
Enter todo ID to mark complete: _
```

**Success Output**:
```
✓ Todo marked as complete!
  ID: 1
  Description: Buy groceries
  Status: Complete
```

**Error Scenarios**:

| Error Condition         | User Message                                          |
|-------------------------|-------------------------------------------------------|
| Non-numeric ID          | "✗ Error: Please enter a valid number."               |
| Todo not found          | "✗ Error: Todo with ID 5 not found. Use 'View All Todos' to see valid IDs." |
| Already complete        | "ℹ️  Todo is already complete." (info, not error)     |

---

### 5. Mark Todo Incomplete

**Menu Option**: 5
**User Input Required**: Todo ID (integer)

**Input Prompt**:
```
Enter todo ID to mark incomplete: _
```

**Success Output**:
```
✓ Todo marked as incomplete!
  ID: 2
  Description: Finish homework
  Status: Incomplete
```

**Error Scenarios**:

| Error Condition         | User Message                                          |
|-------------------------|-------------------------------------------------------|
| Non-numeric ID          | "✗ Error: Please enter a valid number."               |
| Todo not found          | "✗ Error: Todo with ID 5 not found. Use 'View All Todos' to see valid IDs." |
| Already incomplete      | "ℹ️  Todo is already incomplete." (info, not error)   |

---

### 6. Update Todo

**Menu Option**: 6
**User Input Required**: Todo ID (integer), New Description (string)

**Input Prompts**:
```
Enter todo ID to update: _
Enter new description: _
```

**Success Output**:
```
✓ Todo updated successfully!
  ID: 1
  Old Description: Buy groseries
  New Description: Buy groceries
  Status: Incomplete
```

**Error Scenarios**:

| Error Condition         | User Message                                          |
|-------------------------|-------------------------------------------------------|
| Non-numeric ID          | "✗ Error: Please enter a valid number."               |
| Todo not found          | "✗ Error: Todo with ID 5 not found. Use 'View All Todos' to see valid IDs." |
| Empty new description   | "✗ Error: Description cannot be empty."               |
| Too long (>500 chars)   | "✗ Error: Description cannot exceed 500 characters."  |

---

### 7. Delete Todo

**Menu Option**: 7
**User Input Required**: Todo ID (integer)

**Input Prompt**:
```
Enter todo ID to delete: _
Are you sure you want to delete this todo? (y/n): _
```

**Success Output**:
```
✓ Todo deleted successfully!
  ID: 3
  Description: Read Clean Code book
```

**Cancelled Output**:
```
ℹ️  Deletion cancelled.
```

**Error Scenarios**:

| Error Condition         | User Message                                          |
|-------------------------|-------------------------------------------------------|
| Non-numeric ID          | "✗ Error: Please enter a valid number."               |
| Todo not found          | "✗ Error: Todo with ID 5 not found. Use 'View All Todos' to see valid IDs." |
| Invalid confirmation    | "✗ Error: Please enter 'y' or 'n'."                   |

---

### 8. Exit

**Menu Option**: 8
**User Input Required**: None

**Output**:
```
Thank you for using Todo CLI! Goodbye.
```

**Behavior**: Exits the application gracefully (exit code 0)

**Error Scenarios**: None (always succeeds)

---

## Input Validation Rules

### General Rules

1. **Whitespace Handling**:
   - All user input MUST be trimmed (leading/trailing whitespace removed)
   - Empty input after trimming MUST be rejected

2. **Case Sensitivity**:
   - Menu choices are case-insensitive
   - Confirmation prompts (y/n) are case-insensitive

3. **Error Recovery**:
   - Invalid input MUST display error message
   - User MUST be prompted to try again
   - Application MUST NOT crash on invalid input

### Specific Field Validation

**Todo ID**:
- MUST be integer
- MUST be positive (>0)
- Leading zeros ignored (01 = 1)

**Description**:
- MUST be string
- MUST NOT be empty after trim
- MUST NOT exceed 500 characters after trim
- Special characters allowed (UTF-8)

**Menu Choice**:
- MUST be integer in valid range
- Out-of-range shows error and re-prompts

**Confirmation (y/n)**:
- Accepts: y, Y, yes, Yes, YES
- Accepts: n, N, no, No, NO
- Case-insensitive
- Anything else is invalid

## Output Formatting Rules

### Table Format

**Column Alignment**:
- ID: Right-aligned, 3 characters minimum
- Status: Left-aligned, 12 characters
- Description: Left-aligned, no truncation

**Borders**:
- Header separator: dashes (---) for each column
- Column separator: pipe (|) with spaces

**Example**:
```
ID | Status      | Description
---|-------------|------------------------------------------
  1 | Incomplete  | Buy groceries
 42 | Complete    | Finish homework
```

### Message Prefixes

| Type    | Prefix | Example                                    |
|---------|--------|--------------------------------------------|
| Success | ✓      | "✓ Todo added successfully!"               |
| Error   | ✗      | "✗ Error: Description cannot be empty."    |
| Info    | ℹ️      | "ℹ️  Todo is already complete."            |
| Warning | ⚠️      | "⚠️  Warning: This action cannot be undone."|

### Color Coding (Optional Enhancement)

Colors NOT required for Phase I but can be added:
- Success: Green
- Error: Red
- Info: Blue
- Warning: Yellow

## Error Message Catalog

### Input Validation Errors

```python
# Empty input
"✗ Error: Description cannot be empty."

# Too long
"✗ Error: Description cannot exceed 500 characters."

# Invalid number
"✗ Error: Please enter a valid number."

# Out of range
"✗ Error: Please enter a number between 1-{max}."

# Todo not found
"✗ Error: Todo with ID {id} not found. Use 'View All Todos' to see valid IDs."

# Invalid confirmation
"✗ Error: Please enter 'y' or 'n'."
```

### System Errors

```python
# Unexpected error (should never happen with proper validation)
"✗ Error: An unexpected error occurred. Please try again."

# Keyboard interrupt (Ctrl+C)
"\nℹ️  Operation cancelled. Returning to main menu."
```

## User Experience Guidelines

### Responsiveness

- Every user action MUST receive immediate feedback (<5 seconds)
- Long operations (none in Phase I) MUST show progress indicator

### Clarity

- Error messages MUST be specific and actionable
- Success messages MUST confirm what changed
- Prompts MUST clearly indicate expected input format

### Consistency

- Message format MUST be consistent (prefix + message)
- Table format MUST be consistent across all views
- Prompt format MUST be consistent (label + colon + space + cursor)

## Testing Checklist

**Menu Navigation**:
- ✅ Display main menu on startup
- ✅ Accept valid menu choices (1-8)
- ✅ Reject invalid menu choices (0, 9, letters)
- ✅ Loop menu until exit chosen

**Command Execution**:
- ✅ Each command executes correctly
- ✅ Success messages display correctly
- ✅ Error messages display for invalid input
- ✅ Application never crashes on bad input

**Output Formatting**:
- ✅ Tables align correctly
- ✅ Empty states display correctly
- ✅ Long descriptions don't break layout
- ✅ Special characters display correctly (UTF-8)

**Edge Cases**:
- ✅ Empty todo list
- ✅ Single todo
- ✅ Many todos (>50)
- ✅ Very long description (500 chars)
- ✅ Special characters in description
- ✅ Rapid repeated commands

## Example Session

```
=== Todo CLI ===
1. Add Todo
2. View All Todos
3. Filter Todos
4. Mark Todo Complete
5. Mark Todo Incomplete
6. Update Todo
7. Delete Todo
8. Exit

Enter your choice (1-8): 1

Enter todo description: Buy groceries

✓ Todo added successfully!
  ID: 1
  Description: Buy groceries
  Status: Incomplete

=== Todo CLI ===
... (menu repeats)

Enter your choice (1-8): 2

=== All Todos ===

ID | Status      | Description
---|-------------|------------------------------------------
1  | Incomplete  | Buy groceries

Total: 1 todo (0 complete, 1 incomplete)

=== Todo CLI ===
... (menu repeats)

Enter your choice (1-8): 4

Enter todo ID to mark complete: 1

✓ Todo marked as complete!
  ID: 1
  Description: Buy groceries
  Status: Complete

=== Todo CLI ===
... (menu repeats)

Enter your choice (1-8): 8

Thank you for using Todo CLI! Goodbye.
```

## Notes

- Interface designed for Python learners (clear, friendly, forgiving)
- All error messages guide user to correct action
- Confirmation required only for destructive actions (delete)
- Future phases can add more commands without breaking existing interface
