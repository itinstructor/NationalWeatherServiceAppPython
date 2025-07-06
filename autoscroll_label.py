import tkinter as tk


class AutoScrollLabel:
    """This label cannot set it's own size. You must layout this label
    in a place where the container sets the size"""

    def __init__(self, parent=None, **kwargs):
        # Create a frame container to hold the label
        self.frm = tk.Frame(parent)
        
        # Add a spacer label to give the frame some height
        tk.Label(self.frm, text=" ").pack()
        
        # Create the actual label that will display the text and potentially scroll
        # **kwargs allows passing any label properties like text, font, color, etc.
        self.lbl = tk.Label(self.frm, **kwargs)
        
        # Initially position the label centered horizontally at the top
        # relx=0.5 means 50% from left edge, anchor="n" means anchor at north (top center)
        self.lbl.place(relx=0.5, y=0, anchor="n")
        
        # Flag to track if we're currently in scrolling mode
        self.scrolling = False
        
        # Bind to window resize events - whenever the window is resized, check if scrolling is needed
        # The "+" means add this binding without removing existing ones
        tk._default_root.bind("<Configure>", self.scroll_set, "+")
        
        # Store the attributes of tk.Widget to determine which attributes belong to the frame vs label
        # This is used in __getattr__ to properly delegate attribute access
        self.outer_attr = set(dir(tk.Widget))

    def scroll_set(self, event):
        """Check if scrolling is needed when the window is resized.
        
        This method is called whenever a window resize event occurs.
        If the frame width is smaller than the label width, the text won't fit
        and we need to start scrolling.
        """
        # Check if the text is too wide for the container
        if self.frm.winfo_width() < self.lbl.winfo_width():
            # Only start scrolling if we're not already scrolling
            if not self.scrolling:
                # Remove the label from its current centered position
                self.lbl.place_forget()
                
                # Reposition the label at the left edge to start scrolling
                # x=0, y=0 means top-left corner, anchor="nw" means northwest corner
                self.lbl.place(x=0, y=0, anchor="nw")
                
                # Set the scrolling flag and start the scroll animation
                self.scrolling = True
                self.scroll_loop()

    def scroll_loop(self, x=0):
        """Animate the scrolling text by moving it pixel by pixel.
        
        Args:
            x: Current x-position of the label (starts at 0, becomes negative as it scrolls left)
        """
        # Check if the container is now wide enough to fit the text (user resized window larger)
        if self.frm.winfo_width() > self.lbl.winfo_width():
            # Text fits again, so stop scrolling and center the label
            self.lbl.place_forget()
            self.lbl.place(relx=0.5, y=0, anchor="n")  # Back to centered position
            self.scrolling = False
            
        # Check if we've scrolled far enough that the end of the text is visible
        # -x is how far we've moved left, compare to how much text extends beyond the frame
        elif -x > (self.lbl.winfo_width() - self.frm.winfo_width()):
            # We've reached the end, pause for 500ms then restart from the beginning
            self.lbl.after(500, self.scroll_loop, 0)
        else:
            # Continue scrolling: move the label 1 pixel to the left
            self.lbl.place_configure(x=x)
            # Schedule the next frame of animation after 75ms, moving 1 pixel further left
            self.lbl.after(75, self.scroll_loop, x - 1)

    def __getattr__(self, item):
        """Delegate attribute access to either the frame or the label.
        
        This magic method is called when someone tries to access an attribute
        that doesn't exist on the AutoScrollLabel instance itself.
        
        It allows the AutoScrollLabel to behave like either a Frame or Label
        depending on what attribute is being accessed:
        - Widget attributes (like grid, pack, place) go to the frame
        - Label-specific attributes (like text, font, color) go to the label
        
        Args:
            item: The name of the attribute being accessed
            
        Returns:
            The attribute from either self.frm or self.lbl
        """
        return getattr(self.frm if item in self.outer_attr else self.lbl, item)


## DEMO - Example usage of the AutoScrollLabel
root = tk.Tk()
root.columnconfigure(0, weight=1)  # Make the column expandable

# Add a title label
tk.Label(text="Demo program").grid(sticky="ew")

# Create an AutoScrollLabel with long text that will trigger scrolling
label = AutoScrollLabel(
    text="Can anyobody help me make an autoscroll function that achieves this?"
)
# Use sticky="ew" to make the label expand horizontally with the window
label.grid(sticky="ew")

# Start the GUI event loop
root.mainloop()
