* md2do
  * Bugs
    - [x] Check out / Fix the consecutive edits + line bleed errors
  * Action Design
    - [ ] Try using unchanged bullets to give the LLM the opportunity to replace entire paragraphs
  * Voice Conversation
    - [ ] **Split output into natural language and JSON**
    - [x] Add back-and-forth chat-like behaviour (only give the context for how to use the system in the beginning?)
    - [ ] Add voice input
    - Add voice output
  * Scope Extension
    - [ ] Add task / project metadata
    - Add file support (md links?)
    - Add calendar / scheduled items (timestamps?)
    - Add email
  * View Creation
    - Add ability to return a view of the todo.md (expose python functions for filtering with regex? open .tmp file afterwards?)
  * OS-level Integration
    - Add context awareness of active window / row
    - Add continuous listening and trigger word activation
    - Add OS-level hotkey functionality
    - Add menu bar icon
    - Add notification system
  * Git Tracking
    - [ ] Add git commits after change
    - [ ] Add change confirmation via git diff logging (verbal?)
    - Add ability to roll back a commit (is this best practice?)
  * System integration
    - Integrate external calendars
    - Add Web interface
    - Create mobile interface (running on server?)