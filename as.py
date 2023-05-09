'''To add new rows or columns on the left or top edges, you need to modify the world_data list and update the grid drawing functions accordingly.

To add a new row on the top edge, you can use the insert method of the list to insert a new row at index 0, and set all the tile values in the new row to -1 to indicate empty tiles. Here's an example:
'''

new_row = [-1] * MAX_COLS
world_data.insert(0, new_row)
#To add a new column on the left edge, you need to insert a new value at the beginning of each existing row in world_data. Here's an example:


for row in world_data:
    row.insert(0, -1)

#To draw the new row or column, you need to update the draw_grid function to include the new lines. You can do this by adding new for loops that draw the lines for the new row or column, using the same logic as the existing loops.