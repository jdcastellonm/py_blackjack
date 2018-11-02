from tkinter import *
from tkinter import messagebox
# from winsound import *
import game_code
import random
# image taken from http://www.123freevectors.com

def program_exit(event=0):
	if messagebox.askyesno(title = 'Exit', message = 'Are you sure you want to exit?'):
		window.destroy()

def show_gamewindow(event=0):
	global window
	show_game = game_window(window)

def show_funds(event=0):
	messagebox.showinfo(title = 'Your Funds', message = ('Your current funds are: $' + str(game_code.funds)))

def reset_funds(event=0):
	if messagebox.askyesno(title = 'Reset Funds', message = 'Are you sure you want to reset your funds to 0$?'):
		game_code.funds = 0

class game_window():
	# game dialog window object
	def __init__(self, parent):
		#super(game_window, self).__init__()
		top = self.top = Toplevel(master=parent)
		top.title('BLACKJACK')
		top.configure(bg='#0B3B0B')
		top.resizable(width=FALSE, height=FALSE)
		x = (top.winfo_screenwidth()/2) - (400/2)
		y = (top.winfo_screenheight()/2) - (215/2)
		top.geometry(('%dx%d+%d+%d') % (400, 215, x, y))
		top.transient(parent)
		top.grab_set()

		# listbox
		self.listbox = Listbox(top, selectmode = SINGLE)
		self.listbox.grid(row = 0, column = 0, columnspan =2, sticky = W+E)

		# hit me, deal and return buttons
		self.btn_deal = Button(top, text = "Deal", width = 10, command = self.fill_list, underline = 0, bg = 'light green')
		self.btn_deal.grid(row = 2, column = 0, sticky = S)
		self.btn_hitme = Button(top, text = 'Hit Me', width = 10, command = self.hitme, state = DISABLED, underline = 0)
		self.btn_hitme.grid(row = 2, column = 1, sticky = S)
		self.btn_return = Button(top, text = 'Return', command = self.game_exit, bg = 'pink', fg = 'red', underline = 0)
		self.btn_return.grid(row = 3, column = 0, columnspan = 2, sticky = W+E)
		# button accelerators
		top.bind('d', self.fill_list)
		top.bind('r', self.game_exit)

		# score/hand values label
		self.lb_score = Label(top, bg = '#0B3B0B', fg = 'yellow', font = 'Helvetica 13 italic')
		self.lb_score.grid(row = 0, column = 2, columnspan = 3, sticky = W, padx = 5)
		self.lb_score.configure(text = 'Hand value: ')

		# handle the window close [x] button
		top.protocol('WM_DELETE_WINDOW', self.game_exit)

		#set focus to window
		top.focus_force()

	def fill_list(self, event=0):
		# show the generated hand on the listbox
		game_code.game_over = False
		game_code.deal_hand()
		self.listbox.delete(0, END) # clear listbox of previous hand, if any
		self.flashing_counter = 0
		self.lb_score.configure(fg = 'yellow', font = 'Helvetica 13 italic')

		for each_card in game_code.hand:
			self.listbox.insert(END, each_card.get_card())
		
		# disable buttons and binds
		self.btn_deal.configure(state = DISABLED)
		self.btn_return.configure(state = DISABLED)
		self.btn_hitme.configure(state = NORMAL)
		self.top.unbind('d')
		self.top.bind('h', self.hitme)
		self.top.unbind('r')
		self.lb_score.configure(text = ('Hand value: ' + str(game_code.score)))
		self.game_result()

	def hitme(self, event=0):
		# draw another card onto hand
		game_code.hit_me()
		self.listbox.insert(END, game_code.temp_card.get_card())
		self.lb_score.configure(text = ('Hand value: ' + str(game_code.score)))
		self.game_result()

	def game_result(self):
		# re-enable the Deal/return button when a game ends, reset the hand and shuffle the deck
		if game_code.game_over:
			self.btn_hitme.configure(state = DISABLED)
			self.btn_deal.configure(state = NORMAL)
			self.btn_return.configure(state = NORMAL)
			self.top.unbind('h')
			self.top.bind('d', self.fill_list)			
			self.top.bind('r', self.game_exit)

			del game_code.hand[:]
			random.shuffle(game_code.deck)

			if game_code.score == 21:
				self.lb_score.configure(text = ('You got 21!' + '\nYOU WIN $100!'), font = 'Algerian 13 bold')
				# PlaySound('win31_win.wav', SND_FILENAME)  <-- only works on windows
				self.flashing_text()
			else:
				self.lb_score.configure(text = ('Hand value: ' + str(game_code.score) + '\nYou lose $50.\n\nWant to play again?\nPress Deal!'), fg = 'light pink')
				if game_code.funds == -1000:	# game over when player loses 1000$
					messagebox.showerror(title = 'OUT OF FUNDS', message = 'You have lost $1000. GAME OVER!')
					window.destroy()

	def flashing_text(self):
		current_color = self.lb_score.cget('fg')
		next_color = 'light blue' if current_color == 'pink' else 'pink'
		self.lb_score.configure(fg = next_color)
		self.flashing_counter += 1
		if (self.flashing_counter < 15):
			self.top.after(250, self.flashing_text)
	
	def game_exit(self, event=0):
		if game_code.game_over:
			self.top.destroy()
		else:
			messagebox.showwarning(title = 'Game in Progress', message = 'Game is still in progress!')

		


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

window = Tk()

# set up main window
window.title('BLACKJACK') 
window.configure(bg='#0B3B0B')
window.resizable(width=FALSE, height=FALSE)
x = (window.winfo_screenwidth()/2) - (600/2)
y = (window.winfo_screenheight()/2) - (310/2)
window.geometry(('%dx%d+%d+%d') % (600, 310, x, y)) # center on screen
window.protocol('WM_DELETE_WINDOW', program_exit)	# redirect the [x] close button to the program_exit function

# set the image banner
title_image = PhotoImage(file = 'title.png')
title_label = Label(window, image = title_image, bg = '#0B3B0B')
title_label.pack(side = TOP)
#frame = Frame(window, bg = '#0B3B0B')
#frame.pack(side=BOTTOM)
banner = PhotoImage(file ="cards.png")
banner_label =  Label(window, image = banner, bg = '#0B3B0B')
banner_label.pack(side = BOTTOM)

# create the menu
menu = Menu(window)
window.configure(menu = menu)
main_menu = Menu(menu)
menu.add_cascade(label = "Main Menu", menu = main_menu)
main_menu.add_command(label = "Play a Game", command = show_gamewindow, accelerator = "Ctrl+P", underline = 0)
main_menu.add_command(label = "Display Funds", command = show_funds, accelerator = "Ctrl+F", underline = 9)
main_menu.add_command(label = "Reset Funds to $0", command = reset_funds, accelerator = "Ctrl+R", underline = 0)
main_menu.add_separator()
main_menu.add_command(label = "Exit", command = program_exit, accelerator = "Ctrl+E", underline = 0)
# set menu shortcuts
window.bind("<Control-p>", show_gamewindow)
window.bind("<Control-f>", show_funds)
window.bind("<Control-r>", reset_funds)
window.bind("<Control-e>", program_exit)

window.mainloop()

