# -*- coding: utf-8 -*-
"""
PyOpticalTable -- Library for drawing optical layouts. 

Classes
--------------
    tools : helper functions for drawing and aligning optics correctly
    
    OpticalElement : contains info specific to a certain element
    
    OpticalTable : holds all elements, elements are methods of the table
    
    LaserBeam: draws beam between all listed elements
    
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

allowed_types = ('mirror', 'concave_lens', 'convex_lens',
                 'transmissive_plate', 'transmissive_cube',
                 'beamsplitter_cube', 'generic_box',
                 'box_source', 'point_source',
                 'beam_dump', 'generic_circle',
                 'concave_mirror')

allowed_modes = ('r', 't')

allowed_sides = ('top', 'bottom', 'left', 'right')

fontparams = {'fontsize': 8, 'fontweight': 'normal', 'ha': 'center',
              'va': 'center', 'rotation': 'horizontal'}


class Tools:
    """
    Tools contains functions that help with drawing and aligning optics correctly.
    
    Tools is normally not called by the end user, but it is used in other classes
    to ensure optics are placed and rotated correctly.
    """
    def inch_to_mm(x):
        """Convert inches to millimetre."""
        return x*25.4

    def mm_to_inch(x):
        """Convert millimetre to inches."""
        return x/25.4

    def deg_to_rad(x):
        """Convert degrees to radians."""
        return x * (np.pi/180)

    def rotate_point(point, angle, origin=(0,0)):
        """
        Rotate a point by an angle theta around the origin.
        
        Used for rotating optics around their centre. Uses a simple 2D rotation
        matrix (written out in longhand).
        
        Parameters
        ----------
            point : tuple
                Coordinates (x,y) of the point to be rotated relative to (0,0).
            angle : float
                Angle in degrees to rotate the point by.
        Returns
        ----------
            point_rot : tuple
                Coordinates of the rotated point (x_rot, y_rot).
        """
        
        #JDP fixed so it actually rotates about the origin 
        x_rot = (point[0]-origin[0])*np.cos(Tools.deg_to_rad(angle)) - \
            (point[1]-origin[1])*np.sin(Tools.deg_to_rad(angle)) + origin[0]
        
        y_rot = (point[0]-origin[0])*np.sin(Tools.deg_to_rad(angle)) + \
            (point[1]-origin[1])*np.cos(Tools.deg_to_rad(angle)) + origin[1]
        
        point_rot = (x_rot, y_rot)
        return point_rot

    def sind(x):
        """Return sine of an angle in degrees."""
        return np.sin(Tools.deg_to_rad(x))

    def cosd(x):
        """Return cosine of an angle in degrees."""
        return np.cos(Tools.deg_to_rad(x))

    def get_midpoint(line):
        """
        Return the midpoint of a line.
        
        Line is loaded as a tuple of points ( (x1, y1), (x2, y2) )
        
        Parameters
        ----------
            line : tuple
                Contains two points (as tuples (x,y)) that define the line.
        
        Returns
        ----------
            midpoint : tuple
                The midpoint of the line (midpoint_x, midpoint_y)
        """
        point1 = line[0]
        point2 = line[1]
        midpoint_x = 0.5*(point1[0] + point2[0])
        midpoint_y = 0.5*(point1[1] + point2[1])
        midpoint = (midpoint_x, midpoint_y)
        return midpoint

    def get_label_coords(label_pos, x, y, size, labelpad):
        """
        Returns the coordinates where the label for an optic should be.
        
        Calculates them based on the position and size of the optic. User defined
        labelpad can also be used to further move the label. 
        
        Label position is determined by the label_pos parameter.

        Parameters
        ----------
        label_pos : string
            String determining label position relative to the optic. Allowable
            values are 'top', 'bottom', 'left', 'right'.
        x : float
            x-coordinate of the optical element being labelled.
        y : float
            y-coordinate of the optical element being labelled.
        size : float
            size of optical element being labelled.
        labelpad : float
            additional space to put between optic and label.

        Returns
        -------
        label_x : float
            x-coordinate of label position.
        label_y : TYPE
            y-coordinate of label position.

        """
        offset = (size*0.5) + labelpad
        if label_pos == 'top':
            label_x = x
            label_y = y + offset
        elif label_pos == 'bottom':
            label_x = x
            label_y = y - offset
        elif label_pos == 'left':
            label_x = x - offset
            label_y = y
        elif label_pos == 'right':
            label_x = x + offset
            label_y = y
        elif label_pos == 'centre':
            label_x = x
            label_y = y
        else:
            raise ValueError(
                'Invalid label position - should be "top", "bottom", "left", \
                  "right", or "centre".')
        return label_x, label_y


class OpticalElement:
    """
    OpticalElement contains information specific to an optical element.
    
    An instance of this class is created whenever an optical element is added 
    to the table.
    
    Attributes
    -----------
        x : float
            x coordinate of the optical element
        y : float
            y coordinate of the optical element
        mode : 
            mode of the optic - transmissive "t", or reflective "r" (UNUSED)
        angle : float
            rotation angle of the optic relative to the x axis
    """

    def __init__(self, x, y, mode, angle=None, element_type=None):
        if mode not in allowed_modes:
            raise ValueError('Invalid mode type.')

        if element_type not in allowed_types:
            raise ValueError('Invalid element type.')
        self.x = x
        self.y = y
        self.mode = mode
        self.angle = angle


class OpticalTable:
    """
    OpticalTable is where OpticalElements are placed, and forms the main 
    drawing canvas.
    
    Calling OpticalTable will generate a figure to which optics (defined as 
    methods of OpticalTable) will be added.
    
    The length and width determine the internal table coordinates used to place
    optics, and then also determine the final figure size in conjunction with size_factor. 
    Essentially then the coordinates can be made into a sensible range for ease
    of use, and then the final figure size controlled with size_factor. 
    The table is centered on the origin so the coordinates range from -length/2 
    to length/2 and so on.
    
    Parameters
    ----------
        length : int
            Length (x dimension) of the table, in internal figure coordinates.
        width : int
            Width (y dimension) of the table, in internal figure coordinates.
        size_factor : float, optional
            The length and width are each multiplied by the size factor to give
            the dimensions of the final figure in millimetres. The default is 10.
        edgecolour : string, optional
            Colour of the border of the table, any matplotlib supported colour 
            works. The default is 'k' (black).
        grid_spacing : float, optional
            Spacing of lines shown on the table grid, in internal figure coordinates. 
            Must be chosen such that there is an integer number of lines over the length. The default is 1.
        gridcolour : string, optional
            Colour of the grid on the table, any matplotlib supported colour 
            works. The default is 'gray'.
        show_edge : bool, optional
            If true then the edge of the table is shown. The default is True.
        show_grid : bool, optional
            If true then a grid is shown over the table. The default is False.
        show_labels : bool, optional
            If true then coordinate labels are added to the grid. The default 
            is False
            
    Attributes
    ----------
        ax : AxesSubplot
            Matplotlib axis containing the optical table figure.
        aspect_ratio : float
            Ratio of the length to the width of the table.
            
    """

    def __init__(self, length, width, size_factor=10.0, edgecolour='k', grid_spacing=1.0,
                 gridcolour='gray', show_edge=True, show_grid=False, show_labels=False):

        plt.figure(figsize=(Tools.mm_to_inch(length*size_factor), 
                            Tools.mm_to_inch(width*size_factor)),
                            facecolor='w', frameon=False)
        plt.plot([-length/2, length/2], [width/2, width/2],
                 color=edgecolour, visible=show_edge)
        plt.plot([-length/2, length/2], [-width/2, -width/2],
                 color=edgecolour, visible=show_edge)
        plt.plot([length/2, length/2], [-width/2, width/2],
                 color=edgecolour, visible=show_edge)
        plt.plot([-length/2, -length/2], [-width/2, width/2],
                 color=edgecolour, visible=show_edge)
        plt.axis('off')

        if show_grid:
            N_lines_x = length/grid_spacing
            assert N_lines_x.is_integer()
            N_lines_y = width/grid_spacing
            assert N_lines_y.is_integer()

            x_lines = [(-length/2)+(n*grid_spacing)
                       for n in range(int(N_lines_x+1))]
            y_lines = [(-width/2)+(n*grid_spacing)
                       for n in range(int(N_lines_y+1))]

            [plt.plot([line, line], [-width/2, width/2],
                      color=gridcolour, lw=0.5) for line in x_lines]
            [plt.plot([-length/2, length/2], [line, line],
                      color=gridcolour, lw=0.5) for line in y_lines]

            if show_labels:
                [plt.text(line, (-width/2)-1, str(line), ha='center',
                          va='center') for line in x_lines]
                [plt.text((-length/2)-1, line, str(line),
                          ha='center', va='center') for line in y_lines]

        self.ax = plt.gca()
        self.aspect_ratio = length/width

    def angled_line(self, x, y, size, angle, colour='k', show=True, 
                    get_coords=False):
        """
        Generate a line centered at (x, y) of length size, rotated by an angle
        angle (in degrees).
        
        The line automatically scales itself if the aspect ratio is changed.
        
        This function is mostly called by the optical element generation functions
        but can also just be used to put a line somewhere (or get the coordinates of a line).

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the line.
        y : float
            y-coordinate of the centre of the line.
        size : float
            Length of the line.
        angle : float
            Rotation angle of the line anticlockwise from the x-axis, in degrees.
        colour : string, optional
            Colour of the line, any matplotlib supported colour works. 
            The default is 'k' (black).
        show : bool, optional
            If True then the line is plotted on the table. The default is True.
        get_coords : bool, optional
            If True then the coordinates of the two endpoints are returned as 
            (x1, x2, y1, y2). The default is False.

        Returns
        -------
        x-dX : float
            Smaller of the two x coordinates of the line (x1).
        x+dX : float
            Larger of the two x coordinates of the line (x2).
        y-dy : float
            Smaller of the two y coordinates of the line (y1).
        y+dY : float
            Larger of the two y coordinates of the line (y2).

        """
        dX = (size/2) * Tools.cosd(angle) * self.aspect_ratio
        dY = (size/2) * Tools.sind(angle) * self.aspect_ratio
        if show:
            self.ax.plot([x-dX, x+dX], [y-dY, y+dY], color=colour)
        if get_coords:
            return x-dX, x+dX, y-dY, y+dY

    def set_label(self, axis, x, y, size, label, label_pos, labelpad, textcolour='k', fontsize=fontparams['fontsize']):
        """
        Put a label on an optical element. 
        
        If the label is None then this does nothing.
    
        Label coordinates are determined dynamically by the optic coordinates, 
        optic size, and any padding added by the user. The position relative 
        to the optic is determined by passing label_pos ('top', 'bottom', 'left', 'right').

        Parameters
        ----------
        axis : AxesSubplot
            Axis to put the label onto.
        x : float
            x-coordinate of the optic to be labelled.
        y : float
            y-coordinate of the optic to be labelled.
        size : float
            Size of the optic to be labelled.
        label : string
            Text to put in the label.
        label_pos : string
            Position of the label relative to the optic ('top', 'bottom', 'left', 'right').
        labelpad : float
            Additional padding to add between the label and the optic.
        textcolour : string, optional
            Colour of the label text. Default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Returns
        -------
        None.

        """
        if label is not None:
            fontsdict = fontparams.copy()
            fontsdict['fontsize'] = fontsize
            label_x, label_y = Tools.get_label_coords(
                label_pos, x, y, size, labelpad)
            axis.text(label_x, label_y, label, color=textcolour, **fontsdict)

    def mirror(self, x, y, size, angle, colour='k',
               label=None, label_pos='bottom', labelpad=0.25, textcolour='k',
               fontsize=fontparams['fontsize']):
        """
        Draw a mirror on the optical table.
        
        A mirror is simply an angled line. Laser beams will bounce off the 
        middle of the mirror, at the point (x,y).

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the optic.
        y : float
            y-coordinate of the centre of the optic.
        size : float
            Size of the optic.
        angle : float
            Rotation of the optic anticlockwise from the positive x-axis, in degrees.
        colour : string, optional
            Colour of the optic, any matplotlib supported colour works. The default is 'k'.
        label : string, optional
            Text to put in the label for the optic. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the optic ('top', 'bottom', 'left', 'right'). The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the optic. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """
        self.angled_line(x, y, size, angle, colour=colour)
        self.set_label(self.ax, x, y, size, label, label_pos,
                       labelpad, textcolour, fontsize=fontsize)
        return OpticalElement(x, y, 'r', angle, 'mirror')

    def convex_lens(self, x, y, size, angle, colour='k', lens_factor=2,
                    label=None, label_pos='top', labelpad=0.25, textcolour='k',
                    fontsize=fontparams['fontsize']):
        """
        Draw a convex lens on the optical table.

        The beam will pass through the point (x,y), which is the centre of the
        flat face of the lens.        
        
        Parameters
        ----------
        x : float
            x-coordinate of the centre of the flat face of the lens.
        y : float
            y-coordinate of the centre of the flat face of the lens.
        size : float
            Size of the optic.
        angle : float
            Rotation of the optic anticlockwise from the positive x-axis, in degrees.
        colour : string, optional
            Colour of the optic, any matplotlib supported colour works. The default is 'k'.
        lens_factor : float, optional
            Controls how curved the lens is (how "lens-y" it looks). The default is 2.
        label : string, optional
            Text to put in the label for the optic. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the optic ('top', 'bottom', 'left', 'right'). 
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the optic. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """
        self.angled_line(x, y, size, angle, colour=colour)
        self.set_label(self.ax, x, y, size, label, label_pos,
                       labelpad, textcolour, fontsize=fontsize)
        size_arc = self.aspect_ratio * size
        arc = mpl.patches.Arc((x, y), size_arc, size_arc/lens_factor, angle=angle,
                              theta1=0, theta2=180, color=colour)
        self.ax.add_patch(arc)
        return OpticalElement(x, y, 't', angle, 'concave_lens')

    def concave_mirror(self, x, y, size, angle, colour='k', lens_factor=1,
                       label=None, label_pos='top', labelpad=0.25, 
                       textcolour='k', fontsize=fontparams['fontsize']):
        """
        Draw a concave mirror on the optical table.
        
        The beam will hit the mirror at the point (x, y). 

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the optic.
        y : float
            y-coordinate of the centre of the optic.
        size : float
            Size of the optic.
        angle : float
            Rotation of the optic anticlockwise from the positive x-axis, in degrees.
        colour : string, optional
            Colour of the optic, any matplotlib supported colour works. The default is 'k'.
        lens_factor : float, optional
            Controls how curved the mirror is (how "lens-y" it looks). The default is 1.
        label : string, optional
            Text to put in the label for the optic. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the optic ('top', 'bottom', 'left', 'right'). 
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the optic. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].
        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """

        size_width = size * self.aspect_ratio
        size_height = size_width * lens_factor
        # define the turning point on the long axis of ellipse as where the beam hits
        # in absence of rotation
        offset_x = 0
        offset_y = size_height * 0.5
        edge_point_offset = (offset_x, offset_y)

        # rotate the offsets around the center of the ellipse to get the location
        # the beam hits when the mirror is rotated
        # the entered x,y are where the beam will hit, and the mirror is translated to
        # ensure that this is the turning point of the long axis as the mirror is rotated
        edge_point_rot = Tools.rotate_point(edge_point_offset, angle)
        arc = mpl.patches.Arc((x-edge_point_rot[0], y-edge_point_rot[1]), 
                              size_width, size_height, angle=angle,
                              theta1=0, theta2=180, color=colour)
        self.ax.add_patch(arc)
        self.set_label(self.ax, x, y, size, label,
                       label_pos, labelpad, textcolour)

        return OpticalElement(x, y, 'r', angle, 'concave_mirror')

    def concave_lens(self, x, y, size, angle, colour='k', offset_factor=0.05, 
                     lens_factor=4, label=None, label_pos='top', labelpad=0.25, 
                     textcolour='k', fontsize=fontparams['fontsize']):
        """
        Draw a concave lens on the optical table. 
        
        The beam passes through the point (x,y), which is the centre of the curved 
        side of the lens.

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the curved face of the lens.
        y : float
            y-coordinate of the centre of the curved face of the lens.
        size : float
            Size of the optic.
        angle : float
            Rotation of the optic anticlockwise from the positive x-axis, in 
            degrees.
        colour : string, optional
            Colour of the optic, any matplotlib supported colour works. 
            The default is 'k'.
        offset_factor : float, optional
            How thick the concave lens is. The default is 0.05.
        lens_factor : float, optional
            Controls how curved the lens is (how "lens-y" it looks). The default is 4.
        label : string, optional
            Text to put in the label for the optic. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the optic ('top', 'bottom', 'left', 'right'). 
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the optic. 
            The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """

        offset_x = offset_factor * self.aspect_ratio * Tools.sind(angle)
        offset_y = offset_factor * self.aspect_ratio * Tools.cosd(angle)
        coords1 = self.angled_line(
            x+offset_x, y-offset_y, size, angle, get_coords=True)
        coords2 = self.angled_line(
            x-offset_x, y+offset_y, size, angle, show=False, get_coords=True)
        self.ax.plot([coords1[0], coords2[0]], [
                     coords1[2], coords2[2]], color=colour)
        self.ax.plot([coords1[1], coords2[1]], [
                     coords1[3], coords2[3]], color=colour)
        size_arc = self.aspect_ratio * size
        arc = mpl.patches.Arc((x-offset_x, y+offset_y), size_arc, 
                              size_arc/lens_factor, angle=angle,
                              theta1=180, theta2=360, color=colour)
        self.ax.add_patch(arc)
        self.set_label(self.ax, x, y, size, label,
                       label_pos, labelpad, textcolour)
        return OpticalElement(x, y, 't', angle, 'convex_lens')

    def transmissive_plate(self, x, y, size, angle, colour='k', offset_factor=0.05, 
                           fill=False, fillcolour='k', label=None, label_pos='top', 
                           labelpad=0.25, textcolour='k', fontsize=fontparams['fontsize'],
                           zorder=2):
        """
        Draw a transmissive plate on the optical table.
        
        A generic transmissive plate but is useful for waveplates, crystals, 
        filters, windows etc... with appropriate labelling.
        
        The beam passes through the point (x,y), which is at the centre of the plate.

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the optic.
        y : float
            y-coordinate of the centre of the optic.
        size : float
            Size of the optic.
        angle : float
            Rotation of the optic anticlockwise from the positive x-axis, in degrees.
        colour : string, optional
            Colour of the optic, any matplotlib supported colour works. The default is 'k'.
        offset_factor : float, optional
            How thick the transmissive plate is. The default is 0.05.
        fill : bool, optional
            If true then the plate is filled with a colour. The default is False.
        fillcolour : string, optional
            Colour to fill the plate with. The default is 'k'.
        label : string, optional
            Text to put in the label for the optic. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the optic ('top', 'bottom', 'left', 'right'). 
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the optic. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].
        zorder : int, optional
            Zorder for the transmissive plate (controls drawing order). The default is 2.

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """
        offset_x = offset_factor * self.aspect_ratio * Tools.sind(angle)
        offset_y = offset_factor * self.aspect_ratio * Tools.cosd(angle)
        coords1 = self.angled_line(
            x+offset_x, y-offset_y, size, angle, get_coords=True)
        coords2 = self.angled_line(
            x-offset_x, y+offset_y, size, angle, get_coords=True)
        self.ax.plot([coords1[0], coords2[0]], [
                     coords1[2], coords2[2]], color=colour, zorder=zorder)
        self.ax.plot([coords1[1], coords2[1]], [
                     coords1[3], coords2[3]], color=colour, zorder=zorder)
        if fill:
            l1 = [coords1[0], coords1[1]]
            l2 = [coords1[2], coords1[2]]
            l3 = [coords2[2], coords2[2]]
            self.ax.fill_between(l1, l2, l3, color=fillcolour, zorder=zorder)
        self.set_label(self.ax, x, y, size, label, label_pos,
                       labelpad, textcolour, fontsize=fontsize)
        return OpticalElement(x, y, 't', angle, 'transmissive_plate')

    def transmissive_cube(self, x, y, size, angle, colour='k',
                          label=None, label_pos='top', labelpad=0.25, 
                          textcolour='k', fontsize=fontparams['fontsize']):
        """
        Draw a transmissive cube (i.e a square) on the optical table.
        
        The square is centered at (x,y) and the beam passes through the centre.

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the optic.
        y : float
            y-coordinate of the centre of the optic.
        size : float
            Size of the optic.
        angle : float
            Rotation of the optic anticlockwise from the positive x-axis, in degrees.
        colour : string, optional
            Colour of the optic, any matplotlib supported colour works. The default is 'k'.
        label : string, optional
            Text to put in the label for the optic. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the optic ('top', 'bottom', 'left', 'right').
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the optic. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].


        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """

        self.transmissive_plate(
            x, y, size, angle, colour=colour, offset_factor=size*0.5)
        self.set_label(self.ax, x, y, size, label, label_pos,
                       labelpad, textcolour, fontsize=fontsize)
        return OpticalElement(x, y, 't', angle, 'transmissive_cube')

    def beamsplitter_cube(self, x, y, size, angle, direction, colour='k',
                          label=None, label_pos='top', labelpad=0.25, 
                          textcolour='k', fontsize=fontparams['fontsize']):
        """
        

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the optic.
        y : float
            y-coordinate of the centre of the optic.
        size : float
            Size of the optic.
        angle : float
            Rotation of the optic anticlockwise from the positive x-axis, in degrees.
        direction : string
            Direction of the reflective surface in the beamsplitter, allowed 
            values are "L" and "R".
        colour : string, optional
            Colour of the optic, any matplotlib supported colour works. The default is 'k'.
        label : string, optional
            Text to put in the label for the optic. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the optic ('top', 'bottom', 'left', 'right').
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the optic. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Raises
        ------
        ValueError
            Raised if a direction other than "L" or "R" is entered.

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """
        if not direction in ('L', 'R'):
            raise ValueError('Allowed values for direction are "L" and "R".')
        self.transmissive_cube(x, y, size, angle, colour=colour)
        if direction == 'L':
            self.angled_line(x, y, size*np.sqrt(2), angle=angle+45)
        if direction == 'R':
            self.angled_line(x, y, size*np.sqrt(2), angle=angle-45)
        self.set_label(self.ax, x, y, size, label, label_pos,
                       labelpad, textcolour, fontsize=fontsize)
        return OpticalElement(x, y, 't', angle, 'beamsplitter_cube')

    def box(self, x, y, size_x, size_y, angle, colour='k', linestyle='-', standalone=False,
            label=None, label_pos='top', labelpad=0.25, textcolour='k', 
            fontsize=fontparams['fontsize']):
        """
        Create a rectangular box of arbitrary size and rotation angle.
        
        The box can be drawn on the table (if standalone=True), otherwise the
        corner coordinates of the box are returned from the function to use in
        other functions.

        Parameters
        ----------
         x : float
            x-coordinate of the centre of the box.
        y : float
            y-coordinate of the centre of the box.
        size_x : float
            Size of the box in the x direction.
        size_y : float
            Size of the box in the y direction.
        angle : float
            Rotation of the box anticlockwise from the positive x-axis, in degrees.
        colour : string, optional
            Colour of the box edge, any matplotlib supported colour works. The default is 'k'.
        linestyle : string, optional
            Linestyle for the box edge, any matplotlib support style works. Default is '-' (unbroken).
        standalone : bool, optional
            If true then the box is drawn on the table as it is, otherwise just
            the corner coordinates are returned for use in other functions. The default is False.
        label : string, optional
            Text to put in the label for the box. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the box ('top', 'bottom', 'left', 'right'). 
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the box. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic (if standalone=True)
            
        corners_rot : list
            List of the corner coordinates (anticlockwise from bottom left) of
            the box (if standalone=False).

        """
        offset_x = size_x/2  # * self.aspect_ratio #* np.sin(deg_to_rad(angle))
        offset_y = size_y/2  # * self.aspect_ratio #* np.cos(deg_to_rad(angle))

        #the corners are defined as anticlockwise from the bottom left
        corners = ((x-offset_x, y-offset_y), (x+offset_x, y-offset_y),
                   (x+offset_x, y+offset_y), (x-offset_x, y+offset_y))

        corners_rot = [Tools.rotate_point(corner, angle, origin=(x,y)) for corner in corners]

        for i, _ in enumerate(corners_rot[0:-1]):
            self.ax.plot([corners_rot[i][0], corners_rot[i+1][0]],
                         [corners_rot[i][1], corners_rot[i+1][1]], color=colour, ls=linestyle)
            if i == 2:  # JDP catch the final iteration to close the box
                self.ax.plot([corners_rot[i+1][0], corners_rot[0][0]],
                             [corners_rot[i+1][1], corners_rot[0][1]], 
                             color=colour, ls=linestyle)

        if standalone:
            self.set_label(self.ax, x, y, 0, label,
                           label_pos, labelpad, textcolour)
            return OpticalElement(x, y, 't', angle, 'generic_box')
        else:
            return corners_rot

    def box_source(self, x, y, size_x, size_y, angle, output_side, colour='k',
                   label=None, label_pos='top', labelpad=0.25, textcolour='k',
                   fontsize=fontparams['fontsize']):
        """
        Draw a box on the table that a laser beam can come from.

        Box is centered on (x, y), and the beam will come from the midpoint of 
        one of the four sides, determined by the string passed via output_side. 
        Allowed sides are 'top', 'bottom', 'left', 'right'.        

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the box.
        y : float
            y-coordinate of the centre of the box.
        size_x : float
            Size of the box in the x direction.
        size_y : float
            Size of the box in the y direction.
        angle : float
            Rotation of the box anticlockwise from the positive x-axis, in degrees.
        output_side : string
            Which side of the box the beam will come from, allowed values 'top', 
            'bottom', 'left', 'right'.
        colour : string, optional
            Colour of the box edge, any matplotlib supported colour works. The default is 'k'.
        label : string, optional
            Text to put in the label for the box. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the box ('top', 'bottom', 'left', 'right').
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the box. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Raises
        ------
        ValueError
            Raised if an invalid output side is entered.

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """

        if output_side not in allowed_sides:
            raise ValueError('Invalid Output Side.')

        corners = self.box(x, y, size_x, size_y, angle,
                           colour='k', standalone=False)
        if output_side == 'top':
            side = (corners[2], corners[3])
        elif output_side == 'bottom':
            side = (corners[0], corners[1])
        elif output_side == 'left':
            side = (corners[0], corners[3])
        elif output_side == 'right':
            side = (corners[1], corners[2])

        output_point = Tools.get_midpoint(side)
        self.set_label(self.ax, x, y, 0, label, label_pos,
                       labelpad, textcolour, fontsize=fontsize)
        return OpticalElement(output_point[0], output_point[1], 't', angle, 'box_source')

    def point_source(self, x, y,
                     label=None, label_pos='top', labelpad=0.25, textcolour='k',
                     fontsize=fontparams['fontsize']):
        """
        Create a source for a laser beam at (x,y).
        
        The source is not visible on the table, but just serves as a place where
        a beam can emanate from/pass through.

        Parameters
        ----------
        x : float
            x-coordinate of the point.
        y : float
            y-coordinate of the point.
        label : string, optional
            Text to put in the label for the box. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the box ('top', 'bottom', 'left', 'right').
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the box. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """
        if label:
            self.set_label(self.ax, x, y, label, label_pos,
                           labelpad, textcolour, fontsize=fontsize)
        return OpticalElement(x, y, 't', None, 'point_source')

    def beam_dump(self, x, y, size, angle, colour='k', fillcolour='k',
                  label=None, label_pos='top', labelpad=0.25, textcolour='k', 
                  fontsize=fontparams['fontsize']):
        """
        Draw a beam dump on the table.
        
        A beam dump is simply a filled in block where a beam can terminate. 
        The zorder=10 ensures that the beam dump is always drawn on top of the beam, 
        such that it looks like the beam is effectively blocked.

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the optic.
        y : float
            y-coordinate of the centre of the optic.
        size : float
            Size of the optic.
        angle : float
            Rotation of the optic anticlockwise from the positive x-axis, in degrees.
        colour : string, optional
            Colour of the optic, any matplotlib supported colour works. The default is 'k'.
        fillcolour : string, optional
            Colour to fill the block with. The default is 'k'.
        label : string, optional
            Text to put in the label for the box. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the box ('top', 'bottom', 'left', 'right').
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the box. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """
        self.transmissive_plate(
            x, y, size, angle, colour=colour, fill=True, fillcolour=fillcolour, zorder=10)
        self.set_label(self.ax, x, y, size, label, label_pos,
                       labelpad, textcolour, fontsize=fontsize)
        return OpticalElement(x, y, 't', None, 'beam_dump')

    def generic_circle(self, x, y, size, colour='k', fill=False, fillcolour='k',
                       label=None, label_pos='top', labelpad=0.25, textcolour='k', fontsize=fontparams['fontsize']):
        """
        Draw a circle on the optical table centered at (x,y). 
        
        The radius of the circle is determined by the size parameter. 

        Parameters
        ----------
        x : float
            x-coordinate of the centre of the circle.
        y : float
            y-coordinate of the centre of the circle.
        size : float
            Radius of the circle.
        colour : string, optional
            Colour of the edge of the circle. The default is 'k'.
        fill : bool, optional
            If True then the circle is filled with fillcolour. The default is False.
        fillcolour : string, optional
            Colour to fill the circle with. The default is 'k'.
        label : string, optional
            Text to put in the label for the box. The default is None (no label).
        label_pos : string, optional
            Position of the label relative to the box ('top', 'bottom', 'left', 'right').
            The default is "bottom".
        labelpad : float, optional
            Additional padding to add between the label and the box. The default is 0.25.
        textcolour : string, optional
            Colour of the label text. The default is 'k' (black).
        fontsize : float, optional
            Font size for the label text. The default is fontparams['fontsize'].

        Returns
        -------
        OpticalElement
            Instance of the OpticalElement class for this optic.

        """
        circle = mpl.patches.Circle(
            (x, y), radius=size, edgecolor=colour, fill=fill, facecolor=fillcolour)
        self.set_label(self.ax, x, y, size, label, label_pos,
                       labelpad, textcolour, fontsize=fontsize)
        self.ax.add_patch(circle)
        return OpticalElement(x, y, 't', None, 'generic_circle')


class LaserBeam:
    """
    LaserBeam defines a laser beam that goes through the defined setup.
    
    When an instance of LaserBeam is created a beam with the given colour, 
    linewidth, and linestyle is initialised, but not drawn. The beam is drawn 
    when LaserBeam.draw(table, optics) is called. table is the OpticalTable instance 
    to draw the beam onto, and optics is a list of the optics to pass through 
    (in order of first to last hit).
    
    The idea of this is that the beam will be redrawn automatically if any optical
    elements are moved, removing the need to tediously reroute the whole beam by hand. 
    Each OpticalElement instance contains an (x,y) coordinate which is where the beam will hit the optic.
     
    Attributes
    ----------
        colour : string
            Colour of the laser beam, any matplotlib defined colour is fine. 
        width : float, optional
            Linewidth of the drawn laser beam (as defined in matplotlib). 
            The default is 1.
        style : string, optional
            Linestyle of the drawn laser beam, see matplotlib docs for more details.
            The default is '-' (unbroken line).
        divergent : bool, optional
            NOT IMPLEMENTED 
        divergence_angle : float, optional
            NOT IMPLEMENTED
        
    """

    def __init__(self, colour, width=1, style='-', divergent=False, divergence_angle=None):
        self.colour = colour
        self.width = width
        self.style = style
        self.divergent = divergent
        self.div_angle = divergence_angle

    def draw(self, table, optics):
        """
        Draw a laser beam on table between the OpticalElement instances in optics.
        
        The list optics is a list of OpticalElement instances, and the beam originates 
        at the first element in the list, and passes through/reflects off each element 
        sequentially. Thus, the ordering of the list is important to ensure correct beam routing. 
        
        Beam parameters (colour, linewidth, linestyle) are controlled when the 
        LaserBeam class is initialised.

        Parameters
        ----------
        table : OpticalTable
            The instance of OpticalTable the beam is drawn on.
        optics : list
            List of OpticalElement instances.

        Returns
        -------
        None.

        """
        if self.divergent:
            pass  # do this later
        else:
            for i, _ in enumerate(optics[0:-1]):
                table.ax.plot([optics[i].x, optics[i+1].x], [optics[i].y, optics[i+1].y],
                              color=self.colour,
                              linewidth=self.width,
                              linestyle=self.style)
