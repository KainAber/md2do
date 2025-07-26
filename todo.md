* md2do
  * Bugs
    - [x] Check out / Fix the consecutive edits + line bleed errors
  * Quality of Life
    - [ ] Remove all logging from the setup tools or package resources
    - [ ] Extract speech patterns and recording configurations into a separate config file
    - [x] Add logging with various levels (info, debug, etc)
  * Action Design
    - [ ] Add brainstorming capabilities for more conversational AI interactions
    - [ ] Try using unchanged bullets to give the LLM the opportunity to replace entire paragraphs
- Try using unchanged bullets to give the LLM the opportunity to replace entire paragraphs
    - Explore OpenAI build tools
    - [x] Reformat to LLM functions via API
  * Voice Conversation
    - [x] Split output into natural language and JSON
    - Explore OpenAI build tools
    - [x] Add back-and-forth chat-like behaviour (only give the context for how to use the system in the beginning?)
    - [x] Add voice input prototype
    - [ ] Add voice input (also integrate with text input)
    - [x] Add voice output
  * Scope Extension
    - [ ] Add task / project metadata (@tags, #tags etc)
    - Add file support (md links?)
    - Add calendar / scheduled items (timestamps?)
    - Add email
  * View Creation
    - [ ] Add ability to return a view of the todo.md (expose python functions for filtering with regex? open .tmp file afterwards?)
  * OS-level Integration
    - Add context awareness of active window / row
    - Add continuous listening and trigger word activation
    - Add OS-level hotkey functionality
    - Add menu bar icon
    - Add notification system
  * Git Tracking
    - [x] Add git diff logging
    - [x] Add git commits after change
    - [x] Add ability to roll back a commit (is this best practice?)
    - Update rollback feature with a Python command instead of an LLM command
  * System integration
    - Integrate external calendars
    - Add Web interface
    - Create mobile interface (running on server?)