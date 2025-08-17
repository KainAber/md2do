-- SMART LINE INSERTS

-- Mode-preserving smart bullet continuation function
local function smart_insert_line(direction, preserve_insert_mode)
  local line = vim.fn.getline('.')
  local new_line = ''
  
  -- Check for bullet patterns
  if string.match(line, '^%s*%-%s*%[.%]%s') then
    local indent = string.match(line, '^%s*')
    new_line = indent .. '- [ ] '
  elseif string.match(line, '^%s*%-%s') then
    local indent = string.match(line, '^%s*')
    new_line = indent .. '- '
  elseif string.match(line, '^%s*%*%s') then
    local indent = string.match(line, '^%s*')
    new_line = indent .. '* '
  else
    local indent = string.match(line, '^%s*') or ''
    new_line = indent
  end
  
  if direction == 'below' then
    vim.fn.append('.', new_line)
    vim.cmd('normal! j^')
  else
    vim.fn.append(vim.fn.line('.') - 1, new_line)
    vim.cmd('normal! k^')
  end
  
  -- Only enter insert mode if we want to preserve it or if explicitly requested
  if preserve_insert_mode then
    vim.schedule(function()
      vim.cmd('startinsert!')
    end)
  end
end

-- Replace existing mappings with mode-aware versions
vim.keymap.set('i', '<CR>', function()
  smart_insert_line('below', true)  -- Preserve insert mode
end)

vim.keymap.set('n', 'a', function()
  smart_insert_line('above', false)  -- Stay in normal mode
end)

vim.keymap.set('n', 'b', function()
  smart_insert_line('below', false)  -- Stay in normal mode
end)

-- TAB INDENTATION

-- Tab indentation function
local function indent_line(direction)
  local line_num = vim.fn.line('.')
  local line = vim.fn.getline('.')
  local col = vim.fn.col('.')
  
  if direction == 'indent' then
    -- Add 2 spaces at the beginning
    vim.fn.setline(line_num, '  ' .. line)
    -- Adjust cursor position
    vim.fn.cursor(line_num, col + 2)
  else
    -- Remove up to 2 spaces from the beginning
    local new_line = line:gsub('^  ', '', 1)  -- Remove exactly 2 spaces
    if new_line == line then
      new_line = line:gsub('^ ', '', 1)  -- If no 2 spaces, remove 1 space
    end
    vim.fn.setline(line_num, new_line)
    -- Adjust cursor position
    local spaces_removed = #line - #new_line
    vim.fn.cursor(line_num, math.max(1, col - spaces_removed))
  end
end

-- Normal mode mappings
vim.keymap.set('n', '<Tab>', function() indent_line('indent') end)
vim.keymap.set('n', '<S-Tab>', function() indent_line('unindent') end)

-- Insert mode mappings
vim.keymap.set('i', '<Tab>', function() indent_line('indent') end)
vim.keymap.set('i', '<S-Tab>', function() indent_line('unindent') end)

-- TODO BULLET TYPE TOGGLING

-- Todo bullet toggle function
local function toggle_todo()
  local line_num = vim.fn.line('.')
  local line = vim.fn.getline('.')
  local cursor_col = vim.fn.col('.')
  
  -- Extract indentation
  local indent = string.match(line, '^%s*') or ''
  local rest_of_line = string.match(line, '^%s*(.*)') or ''
  
  local new_line
  
  if string.match(rest_of_line, '^%-%s*%[x%]%s*(.*)') then
    -- [x] -> regular bullet
    local content = string.match(rest_of_line, '^%-%s*%[x%]%s*(.*)')
    new_line = indent .. '- ' .. content
  elseif string.match(rest_of_line, '^%-%s*%[%s%]%s*(.*)') then
    -- [ ] -> [x]
    local content = string.match(rest_of_line, '^%-%s*%[%s%]%s*(.*)')
    new_line = indent .. '- [x] ' .. content
  elseif string.match(rest_of_line, '^%-%s*(.*)') then
    -- regular bullet -> [ ]
    local content = string.match(rest_of_line, '^%-%s*(.*)')
    new_line = indent .. '- [ ] ' .. content
  else
    -- No bullet -> regular bullet
    new_line = indent .. '- ' .. rest_of_line
  end
  
  vim.fn.setline(line_num, new_line)
  vim.fn.cursor(line_num, cursor_col)
end

-- Map 't' in normal mode
vim.keymap.set('n', 't', toggle_todo)

-- Override the comment color to be more visible
vim.cmd("highlight Comment ctermfg=8")

-- VISUALS

-- Ensure markdown syntax is loaded first, then add custom highlights
vim.schedule(function()
  -- Add Important highlight group
  vim.cmd("highlight Important cterm=bold")
  vim.cmd("syntax match Important /^.*!.*$/")
  
  -- Add Done highlight group  
  vim.cmd("highlight Done ctermfg=8")
  vim.cmd("syntax match Done /^.*- \\[x\\].*$/")
end)

-- RENAME SAVES

-- Auto-rename file based on first line
local function rename_file_from_first_line()
  local first_line = vim.fn.getline(1)
  
  -- Strip markdown syntax and whitespace
  local clean_name = first_line
    :gsub('^%s*#+%s*', '')   -- Remove leading # characters and whitespace
    :gsub('%s+$', '')        -- Remove trailing whitespace
    :gsub('[:/]', '')        -- Remove macOS problematic characters : and /
  
  if clean_name == '' then return end
  
  local current_file = vim.fn.expand('%:p')
  local dir = vim.fn.expand('%:p:h')
  local new_file = dir .. '/' .. clean_name .. '.md'
  
  -- Only rename if the new name is different and file exists
  if current_file ~= new_file and vim.fn.filereadable(current_file) == 1 then
    -- Save current buffer first
    vim.cmd('write')
    -- Rename the file
    vim.fn.rename(current_file, new_file)
    -- Update buffer name and mark as unmodified
    vim.cmd('file ' .. vim.fn.fnameescape(new_file))
    vim.cmd('set nomodified')
  end
end

-- Trigger rename when leaving insert mode or saving
vim.api.nvim_create_autocmd({'InsertLeave', 'BufWritePre'}, {
  buffer = 0,
  callback = rename_file_from_first_line
})
