# Route Map

## Available Routes


### Admin Blueprint

- `admin.dashboard` → `/dashboard`
- `admin.manage_users` → `/users`
- `admin.system_dashboard` → `/dashboard`
- `admin.verify_documents` → `/documents`

### Attendance Blueprint

- `attendance.scan` → `/scan`

### Auth Blueprint

- `auth.change_password` → `/change-password`
- `auth.login` → `/login`
- `auth.logout` → `/logout`
- `auth.register` → `/register`
- `auth.signup` → `/signup`

### Event_Admin Blueprint

- `event_admin.approve_event` → `/event-admin/events/<int:event_id>/approve`
- `event_admin.dashboard_hyphenated` → `/event-admin/dashboard`
- `event_admin.event_detail_hyphenated` → `/event-admin/events/<int:event_id>`
- `event_admin.events_list` → `/event-admin/events`
- `event_admin.reject_event` → `/event-admin/events/<int:event_id>/reject`

### Events Blueprint

- `events.detail` → `/<int:event_id>`
- `events.list_events` → `/`

### Forum Blueprint

- `forum.list_forums` → `/`
- `forum.view` → `/<int:forum_id>`
- `forum.view_forum` → `/<int:forum_id>`
- `forum.view_post` → `/post/<int:post_id>`

### Group Blueprint

- `group.list_groups` → `/`
- `group.view_group` → `/<int:group_id>`

### Message Blueprint

- `message.compose` → `/compose`
- `message.inbox` → `/inbox`

### Messaging Blueprint

- `messaging.messages_inbox_alias` → `/messages`
- `messaging.read_message_alias` → `/messages/<int:message_id>`
- `messaging.send_message_alias` → `/messages/send`

### Profile Blueprint

- `profile.followers` → `/followers/<int:user_id>`
- `profile.my_events` → `/profile/my-events`
- `profile.view` → `/<int:user_id>`

### Search Blueprint

- `search.search` → `/`

### System Blueprint

- `system.dashboard` → `/dashboard`
- `system.verify_documents` → `/documents`

### System_Manager Blueprint

- `system_manager.approve_event_hyphenated` → `/system-manager/events/<int:event_id>/approve`
- `system_manager.approve_verification_hyphenated` → `/system-manager/verifications/<int:qual_id>/approve`
- `system_manager.create_user_hyphenated` → `/system-manager/users/create`
- `system_manager.dashboard_hyphenated` → `/system-manager/dashboard`
- `system_manager.event_reports` → `/system-manager/reports/events`
- `system_manager.user_reports` → `/system-manager/reports/users`

### User Blueprint

- `user.edit_profile` → `/edit`
- `user.follow_user` → `/<int:user_id>/follow`
- `user.view_profile` → `/<int:user_id>`
