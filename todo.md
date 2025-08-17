# todo

* md2do
  * Bugs
    - [x] Check out / Fix the consecutive edits + line bleed errors#
  * Neovim
    - [x] Copy and paste (just use ctrl)
    - [x] Loop back with arrow keys
    - [x] Add jupyter notebook shortcuts for normal mode (abxcvudzy)
    - [x] Set normal mode beginning of line, insert at end of line
    - [x] Add toggling todos in normal mode
    - [x] Add smart Enter in insert / smart a/b in normal mode
    - [x] Add tab/shift tab in both insert and normal mode
    - [x] Add syntax highlighting (done todos, important todos)
    - [x] Fix md syntax highlighting bug !
    - [ ] Add text conceals for md stuff (beware of bold bullets)
    - [x] Change smart newline behaviour for insert mode (now only for md)
    - [x] Update deletion in normal mode
    - [ ] Try to redo the c v x commands to use CMD
    - Add sync of title and first line for md files
    - Add text selection with modifiers (shift=word-wise, option+ctrl in use)
    - Add treesitter syntax highlighting
  * Quality of Life
    - [x] Research a markdown viewer/editor for this setup
    - [ ] Remove all logging from the setup tools or package resources
    - [ ] Extract speech patterns and recording configurations into a separate config file
    - [x] Add logging with various levels (info, debug, etc)
  * Action Design
    - [ ] Add brainstorming capabilities for more conversational AI interactions
    - Try using unchanged bullets to give the LLM the opportunity to replace entire paragraphs
    - Explore OpenAI build tools
    - [x] Reformat to LLM functions via API
  * Voice Conversation
    - [x] Split output into natural language and JSON
    - Explore OpenAI build tools
    - [x] Add back-and-forth chat-like behaviour (only give the context for how to use the system in the beginning?)
    - [x] Add voice input prototype
    - [ ] Add voice input proper (have the ability to also do text input)
    - [x] Add voice output
  * Scope Extension
    - [ ] Add task / project metadata (@tags, #tags etc)
    - Add file support (md links?)
    - Add calendar / scheduled items (timestamps?)
    - Add email
  * View Creation
    - [ ] **Add ability to return a view of the todo.md** (first test = filter by task type; expose python functions for filtering with regex? open .tmp file afterwards? keep files updated, i.e., refresh .tmp files based on function calls (=names?))
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