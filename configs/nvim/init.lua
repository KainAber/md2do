-- VISUALS

vim.opt.wrap = true
vim.opt.linebreak = true
vim.opt.fillchars = { eob = " " }

-- Override the comment color to be more visible
vim.cmd("highlight Comment ctermfg=8")

-- Show cursor line
vim.opt.cursorline = true

-- Change the cursorline color 
vim.cmd("highlight CursorLine ctermbg=15")


-- Only show cursorline in normal mode
vim.api.nvim_create_autocmd({"InsertEnter"}, {
  callback = function() vim.opt.cursorline = false end
})

vim.api.nvim_create_autocmd({"InsertLeave"}, {
  callback = function() vim.opt.cursorline = true end
})

-- UTILITIES

-- Disable automatic comment continuation
vim.opt.formatoptions:remove({ 'c', 'r', 'o' })

-- Autosave + config reload when leaving insert mode
vim.keymap.set('i', '<Esc>', '<Esc>0:w<CR>:luafile $MYVIMRC<CR>')
-- Reloading to be removed at some point, also then removing the filetype specific reloading at the end of init.lua

-- Write and quit when escaping normal mode
vim.keymap.set('n', '<Esc>', ':wq<CR>')

-- NAVIGATION

-- Allow cursor to move to previous/next line when at beginning/end
vim.opt.whichwrap:append('<,>,h,l,[,]')

-- In normal mode, the cursor is stuck at the beginning
vim.keymap.set('n', '<Left>', '7k0')
vim.keymap.set('n', '<Right>', '7j0')
vim.keymap.set('n', '<S-Left>', '0')
vim.keymap.set('n', '<S-Right>', '0')
vim.keymap.set('n', '<Up>', '0<Up>0')
vim.keymap.set('n', '<Down>', '0<Down>0')


-- SHORTCUTS

-- Disable ALL letter keys in normal mode
for i = 1, 26 do
  vim.keymap.set('n', string.char(96 + i), '<Nop>')  -- a-z
  vim.keymap.set('n', string.char(64 + i), '<Nop>')  -- A-Z
  vim.keymap.set('v', string.char(96 + i), '<Nop>')  -- a-z
  vim.keymap.set('v', string.char(64 + i), '<Nop>')  -- A-Z
end

-- Disable # key
vim.keymap.set('n', '#', '<Nop>')

-- Jupyter-like shortcuts in normal mode
vim.keymap.set('n', '<CR>', '$a')
vim.keymap.set('n', 'a', 'O<Esc>')
vim.keymap.set('n', 'b', 'o<Esc>')
vim.keymap.set('n', 'x', '"+dd')
vim.keymap.set('n', 'c', '"+yy')
vim.keymap.set('n', 'v', '"+P')
vim.keymap.set('n', 'u', ':m .-2<CR>')
vim.keymap.set('n', 'd', ':m .+1<CR>')
vim.keymap.set('n', 'z', 'u')
vim.keymap.set('n', 'y', '<C-r>')
vim.keymap.set('n', 's', ':w<CR>')

-- COPY, PASTE, DELETION

-- Select all in insert mode
vim.keymap.set('i', '<C-a>', '<Esc>ggVG', { noremap = true })

-- Copy and paste with Ctrl modifier
vim.keymap.set('v', '<C-c>', '"+y')
vim.keymap.set('v', '<C-x>', '"+d')
vim.keymap.set('n', '<C-v>', '"+p')  -- In normal mode, paste after cursor
vim.keymap.set('i', '<C-v>', '<C-o>"+P')  -- In insert mode, paste at cursor

-- Add deletion in visual and normal mode
vim.keymap.set('v', '<BS>', 'd')
vim.keymap.set('n', '<BS>', '"+ddk')


-- Trigger filetype events to reload ftplugin files
vim.cmd('doautocmd FileType')
