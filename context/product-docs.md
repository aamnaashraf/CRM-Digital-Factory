# TaskFlow Product Documentation

## Getting Started

### Creating Your First Project
1. Click the "+" button in the sidebar or press `Cmd/Ctrl + N`
2. Enter a project name and optional description
3. Choose a view template: Kanban, List, Timeline, or Calendar
4. Invite team members by email or share the project link
5. Start adding tasks!

### Task Management

#### Creating Tasks
Tasks are the building blocks of your projects. To create a task:
- Click "Add Task" in any project view
- Enter a task title (required)
- Add optional details: description, assignee, due date, priority, tags
- Press Enter or click "Create"

**Quick Add:** Type `/` in any project to open the quick add menu.

#### Task Properties
- **Title:** Brief description of the work (required)
- **Description:** Detailed information, supports Markdown formatting
- **Assignee:** Team member responsible (can assign multiple people)
- **Due Date:** Deadline for completion, triggers reminders
- **Priority:** Low, Medium, High, Urgent (color-coded)
- **Status:** Custom statuses per project (default: To Do, In Progress, Done)
- **Tags:** Custom labels for categorization
- **Attachments:** Upload files up to 100MB (Pro/Business: 500MB)
- **Subtasks:** Break down complex tasks into smaller steps
- **Time Estimate:** Expected hours/days to complete

#### Task Dependencies
Link tasks to show relationships:
- **Blocks:** This task must finish before another can start
- **Blocked By:** This task can't start until another finishes
- **Related To:** Informational link between tasks

Access via the "..." menu on any task → "Add Dependency"

### Views and Layouts

#### Kanban Board
Visual workflow with drag-and-drop columns. Perfect for agile teams.
- Customize column names and order
- Set WIP (Work In Progress) limits per column
- Collapse/expand columns for focus
- Filter by assignee, tag, or priority

#### List View
Traditional task list with sortable columns. Best for detailed task management.
- Sort by any property (due date, priority, assignee)
- Group by status, assignee, or tags
- Bulk edit multiple tasks at once
- Export to CSV

#### Timeline (Gantt Chart)
Visualize project schedule and dependencies. Ideal for complex projects.
- Drag to adjust task duration
- See critical path automatically
- Zoom in/out for different time scales (days, weeks, months)
- Identify scheduling conflicts

#### Calendar View
See all tasks with due dates in a monthly/weekly calendar.
- Drag tasks to reschedule
- Color-coded by project or priority
- Sync with Google Calendar or Outlook
- Set recurring tasks

### Collaboration Features

#### Comments and Mentions
- Click any task to open the detail panel
- Add comments in the "Activity" section
- Use `@username` to mention team members (they'll get notified)
- Use `@here` to notify all project members
- Attach files, images, or links to comments
- Edit or delete your own comments

#### Real-Time Updates
TaskFlow uses WebSocket connections for instant updates:
- See who's viewing the same task (avatars in top-right)
- Live cursor positions when multiple people edit
- Automatic conflict resolution for simultaneous edits
- Offline mode: changes sync when reconnected

#### File Attachments
- Drag and drop files onto tasks or comments
- Supported formats: Images, PDFs, Office docs, code files, videos
- Preview images and PDFs in-app
- Version history for uploaded files (Business tier)

### Integrations

#### Slack Integration
Connect TaskFlow to Slack to:
- Get notifications for task assignments, comments, due dates
- Create tasks from Slack messages (use `/taskflow` command)
- Update task status without leaving Slack
- Daily digest of your tasks sent to DM

**Setup:** Settings → Integrations → Slack → "Connect Workspace"

#### Google Calendar Sync
Two-way sync between TaskFlow and Google Calendar:
- Tasks with due dates appear as calendar events
- Changes in either system sync automatically
- Choose which projects to sync
- Set default event duration

**Setup:** Settings → Integrations → Google Calendar → "Authorize Access"

#### GitHub Integration
Link GitHub issues and pull requests to TaskFlow tasks:
- Auto-create tasks from new GitHub issues
- Update task status when PR is merged
- See commit history in task activity feed
- Supports multiple repositories

**Setup:** Settings → Integrations → GitHub → "Install GitHub App"

#### API Access
TaskFlow provides a REST API for custom integrations:
- Full CRUD operations on projects, tasks, comments
- Webhook support for real-time events
- Rate limits: 1000 requests/hour (Pro), 5000/hour (Business)
- API documentation: developers.taskflow.io

### Automation

#### Automation Rules
Create custom rules to automate repetitive work:
- **Triggers:** When task is created, status changes, due date approaches, etc.
- **Conditions:** If assignee is X, priority is High, tag contains Y, etc.
- **Actions:** Change status, assign to user, add comment, send notification, etc.

**Example Rules:**
- When task is moved to "Done" → Add comment "Great work!" and notify assignee
- When due date is tomorrow → Change priority to High and notify assignee
- When task is created with tag "bug" → Assign to QA team and set priority to Urgent

**Setup:** Project Settings → Automation → "Create Rule"

#### Recurring Tasks
Set tasks to repeat automatically:
- Daily, weekly, monthly, or custom intervals
- Option to create next instance when current is completed
- Useful for standup meetings, weekly reports, monthly reviews

### Mobile Apps

#### iOS and Android
Full-featured native apps available on App Store and Google Play:
- All desktop features available on mobile
- Offline mode with automatic sync
- Push notifications for mentions and due dates
- Quick capture: Create tasks via share sheet or widget
- Biometric authentication (Face ID, Touch ID, fingerprint)

#### Mobile-Specific Features
- **Voice Input:** Dictate task titles and descriptions
- **Photo Attachments:** Capture and attach photos directly
- **Location Tags:** Add location to tasks (optional)
- **Home Screen Widgets:** See today's tasks at a glance

### Reporting and Analytics

#### Dashboard Metrics
- **Task Completion Rate:** Percentage of tasks completed on time
- **Team Velocity:** Average tasks completed per week
- **Burndown Chart:** Progress toward project completion
- **Workload Distribution:** Tasks per team member
- **Overdue Tasks:** Count and list of past-due items

#### Custom Reports
Create custom reports with filters:
- Date range selection
- Filter by project, assignee, tag, priority
- Export to PDF or CSV
- Schedule automated email delivery (Business tier)

### Account and Billing

#### Managing Your Subscription
- View current plan and usage: Settings → Billing
- Upgrade/downgrade anytime (prorated automatically)
- Add or remove users (billing updates next cycle)
- Payment methods: Credit card, PayPal, ACH (Enterprise)
- Invoices available for download in Billing section

#### User Management
- Invite users: Settings → Team → "Invite Member"
- Set roles: Admin, Member, Guest (view-only)
- Deactivate users to free up seats
- SSO (Single Sign-On) available on Business and Enterprise tiers

### Troubleshooting

#### Common Issues

**Slack notifications not working:**
- Verify Slack integration is connected: Settings → Integrations
- Check notification preferences in Slack app
- Re-authorize the integration if needed

**Google Calendar sync delayed:**
- Sync happens every 15 minutes (not real-time)
- Force sync: Settings → Integrations → Google Calendar → "Sync Now"
- Check that calendar permissions are granted

**Mobile app not syncing:**
- Ensure you're connected to internet
- Force close and reopen the app
- Check app permissions in device settings
- Update to latest app version

**Can't upload files:**
- Check file size limits (100MB Free/Pro, 500MB Business)
- Verify file format is supported
- Clear browser cache and try again
- Check storage quota: Settings → Usage

#### Getting Help
- **Help Center:** help.taskflow.io (searchable knowledge base)
- **Email Support:** support@taskflow.io
- **WhatsApp:** +1-512-555-0199 (text only, no calls)
- **Web Form:** taskflow.io/support
- **Status Page:** status.taskflow.io (system uptime and incidents)

**Response Times:**
- Free tier: Best effort (24-48 hours)
- Pro/Business: <4 hours during business hours
- Enterprise: <1 hour, 24/7 coverage
