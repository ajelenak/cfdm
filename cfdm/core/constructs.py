from builtins import (object, str)
from past.builtins import basestring

from collections import OrderedDict
from copy import copy

class Constructs(object):
    '''<TODO>

.. versionadded:: 1.7.0

    '''
    
    def __init__(self, 
                 auxiliary_coordinate=None,                
                 dimension_coordinate=None,         
                 domain_ancillary=None,         
                 field_ancillary=None,         
                 cell_measure=None,
                 coordinate_reference=None,
                 domain_axis=None,
                 cell_method=None,
                 source=None,
                 copy=True,
                 _use_data=True,
                 _view=False,
                 _ignore=()):
        '''<TODO>

:Parameters:

        '''
        self._ignore = tuple(set(_ignore))
    
        if source is not None:
            if _view:
                self._key_base             = source._key_base
                self._array_constructs     = source._array_constructs
                self._non_array_constructs = source._non_array_constructs
                self._ordered_constructs   = source._ordered_constructs
                self._construct_axes       = source._construct_axes
                self._construct_type       = source._construct_type
                self._constructs           = source._constructs
                return
            
            self._key_base             = source._key_base.copy()
            self._array_constructs     = source._array_constructs.copy()
            self._non_array_constructs = source._non_array_constructs.copy()
            self._ordered_constructs   = source._ordered_constructs.copy()
            self._construct_axes       = source._construct_axes.copy()           
            self._construct_type       = source._construct_type.copy()
            self._constructs           = source._constructs.copy()

            for construct_type in self._ignore:
                self._key_base.pop(construct_type, None)
                self._array_constructs.discard(construct_type)
                self._non_array_constructs.discard(construct_type)
                self._ordered_constructs.discard(construct_type)
            
            d = {}            
            for construct_type in source._array_constructs:
                if construct_type in self._ignore:
                    for cid in source._constructs[construct_type]:
                        self._construct_axes.pop(cid, None)
                        self._construct_type.pop(cid, None)
                    continue
                
                if copy:
                    new_v = {}
                    for cid, construct in source._constructs[construct_type].items():
                        new_v[cid] = construct.copy(data=_use_data)
                else:
                    new_v = source._constructs[construct_type].copy()
                    
                d[construct_type] = new_v
            #--- End: for
            
            for construct_type in source._non_array_constructs:
                if construct_type in self._ignore:
                    for cid in source._constructs[construct_type]:
                        self._construct_type.pop(cid, None)
                    continue
                
                if copy:
                    new_v = {
                        cid: construct.copy()
                        for cid, construct in source._constructs[construct_type].items()}
                else:
                    new_v = source._constructs[construct_type].copy()

                d[construct_type] = new_v
            #--- End: for
        
            self._constructs = d

            self._ignore = ()
            
            return
        #--- End: if
        
        self._key_base = {}

        self._array_constructs     = set()
        self._non_array_constructs = set()
        self._ordered_constructs   = set()

        self._construct_axes = {}

        # The construct type for each key. For example:
        # {'domainaxis1':'domain_axis', 'aux3':'auxiliary_coordinate'}
        self._construct_type = {}
        
        self._constructs     = {}
        
        if auxiliary_coordinate:
            self._key_base['auxiliary_coordinate'] = auxiliary_coordinate
            self._array_constructs.add('auxiliary_coordinate')
            
        if dimension_coordinate:
            self._key_base['dimension_coordinate'] = dimension_coordinate
            self._array_constructs.add('dimension_coordinate')
            
        if domain_ancillary:
            self._key_base['domain_ancillary'] = domain_ancillary
            self._array_constructs.add('domain_ancillary')
            
        if field_ancillary:
            self._key_base['field_ancillary'] = field_ancillary
            self._array_constructs.add('field_ancillary')

        if cell_measure:
            self._key_base['cell_measure'] = cell_measure
            self._array_constructs.add('cell_measure')

        if domain_axis:
            self._key_base['domain_axis'] = domain_axis
            self._non_array_constructs.add('domain_axis')

        if coordinate_reference:
            self._key_base['coordinate_reference'] = coordinate_reference
            self._non_array_constructs.add('coordinate_reference')

        if cell_method:
            self._key_base['cell_method'] = cell_method
            self._non_array_constructs.add('cell_method')
            self._ordered_constructs.add('cell_method')

        for x in self._array_constructs:
            self._constructs[x] = {}
        
        for x in self._non_array_constructs:
            self._constructs[x] = {}
        
        for x in self._ordered_constructs:
            self._constructs[x] = OrderedDict()
    #--- End: def

    def __deepcopy__(self, memo):
        '''Called by the `copy.deepcopy` standard library function.

.. versionadded:: 1.7.0

        '''
        return self.copy()
    #--- End: def
   
    def __contains__(self, key):
        '''
        '''
        return key in self._construct_type        
    #--- End: def
    
    def __getitem__(self, key):
        '''
        '''
        construct_type = self.construct_type(key) # ignore??
        if construct_type is None:
            raise KeyError(key)
        
        d = self._constructs.get(construct_type)
        if d is None:
            d = {}
            
        return d[key]
    #--- End: def
  
    def __iter__(self):
        '''
        '''
        return iter(self._dictionary().keys())
    #--- End: def'
            
    def __len__(self):
        '''<TODO>

.. versionadded:: 1.7.0

        '''
        return len(self._dictionary())
    #--- End: def
    
    def __repr__(self):
        '''x.__repr__() <==> repr(x)

        '''
        return '<{0}: {1}>'.format(self.__class__.__name__, str(self))
    #--- End: def

    def __str__(self):
        '''x.__str__() <==> str(x)

        '''
        return 'TODO'
    #--- End: def
    
    # ----------------------------------------------------------------
    # Private methods
    # ----------------------------------------------------------------
    def _default(self, default, message=None):
        '''<TODO>

.. versionadded:: 1.7.0

:Parameters:

    default: 
        <TODO>
        
    message: `str`, optional 
        <TODO>
        
:Returns:

    <TODO>

**Examples:**

<TODO>

        '''
        if isinstance(default, Exception):
            if message is not None and not default.args:
                default = copy(default)
                default.args = (message,)

            raise default
        
        return default
    #--- End: def
    
    # ----------------------------------------------------------------
    # Private dictionary-like methods    
    # ----------------------------------------------------------------
    def _pop(self, key, *default):
        '''D.pop(k[,d]) -> v, remove specified key and return the corresponding value.

If key is not found, d is returned if given, otherwise KeyError is
raised

        '''
        # Remove the construct axes, if any
        self._construct_axes.pop(key, None)

        # Find the construct type
        try:
            construct_type = self._construct_type.pop(key)
        except KeyError as error:
            if default:
                return default[0]
            
            raise KeyError(error)
            
        # Remove and return the construct
        return self._constructs[construct_type].pop(key, *default)
    #--- End: def

#    def _popitem(self):
#        '''
#        '''
#        key, value = self._dictionary()
#
#        # Remove the construct axes, if any
#        self._construct_axes.pop(key, None)
#
#        # Find the construct type
#        try:
#            construct_type = self._construct_type.pop(key, None)
#        except KeyError as error:
#            if default:
#                return default[0]
#            
#            raise KeyError(error)
#            
#        # Remove and return the construct
#        del self._constructs[construct_type]
#
#        return key, value
#    #--- End: def

    def _update(self, other):
        '''D.update(E) -> None. Update D from E.

        '''
        self._ignore = tuple(set(self._ignore).union(other._ignore))

        self._key_base.update            (other._key_base)
        self._array_constructs.update    (other._array_constructs)
        self._non_array_constructs.update(other._non_array_constructs)
        self._ordered_constructs.update  (other._ordered_constructs)
        self._construct_axes.update      (other._construct_axes)
        self._construct_type.update      (other._construct_type)
        self._constructs.update          (other._constructs)
    #--- End: def

    def construct_type(self, key):
        '''TODO
        '''
        x = self._construct_type.get(key)
        if x in self._ignore:
            return
        
        return x
    #--- End: def

    # ----------------------------------------------------------------
    # Private methods    
    # ----------------------------------------------------------------
    def _check_construct_type(self, construct_type):
        '''<TODO>

.. versionadded:: 1.7.0

:Parameters:

    construct_type: `str`

:Returns:

    TODO

**Examples:**

TODO

        '''
        if construct_type is None:
            return None

        x = self._key_base
        if self._ignore:
            x = set(x).difference(self._ignore)
        
        if construct_type not in x:
            raise ValueError(
                "Invalid construct type {!r}. Must be one of {}".format(
                    construct_type, sorted(x)))

        return construct_type    
    #--- End: def

    def _construct_type_description(self, construct_type):
        '''TODO
        '''
        return construct_type.replace('_', ' ')
    #--- End: def

#    def _set_construct_axes(self, key, axes):
#        '''TODO
#        '''
#        self._construct_axes[key] = tuple(axes)
#    #--- End: def

    def _dictionary(self, copy=False):
        '''
        '''
        out = {}
        ignore = self._ignore
        for key, value in self._constructs.items():
            if key not in ignore:
                out.update(value)
        #--- End: if

        if copy:
            for key, construct in list(out.items()):
                out[key] = construct.copy()
        #--- End: if

        return out
    #--- End: def'

    def _del_construct(self, key):        
        '''Remove a construct.

If a domain axis construct is selected for removal then it can't be
spanned by any metdata construct data arrays, nor be referenced by any
cell method constructs. However, a domain ancillary constructs may be
removed even if it is referenced by coordinate reference coinstruct.

.. versionadded:: 1.7.0

.. seealso:: `_get_construct`, `_set_construct`

:Parameters:

   key: `str`
        The key of the construct to be removed.

        *Parameter example:*
          ``key='auxiliarycoordinate0'``
  
:Returns:

        The removed construct, or `None` if the given key did not
        exist.

**Examples:**

>>> x = f.del_construct('auxiliarycoordinate2')

        '''
        data_axes = self.data_axes()
        if key in self.type('domain_axis'):
            # Fail if the domain axis construct is spanned by a data
            # array
            for xid, axes in data_axes.items():
                if key in axes:
                    raise ValueError(
"Can't remove domain axis construct {!r} that spans the data array of {!r}".format(
    key, self.get_construct(key=xid)))
    
            # Fail if the domain axis construct is referenced by a
            # cell method construct
            try:
                cell_methods = self.type('cell_method')
            except ValueError:
                # Cell methods are not possible for this Constructs
                # instance
                pass
            else:
                for xid, cm in cell_methods.items():
                    axes = cm.get_axes(())
                    if key in axes:
                        raise ValueError(
"Can't remove domain axis construct {!r} that is referenced by {!r}".format(
    key, cm))
        else:
            # Remove references to the removed construct in coordinate
            # reference constructs
            for ref in self.type('coordinate_reference').values():
                coordinate_conversion = ref.coordinate_conversion
                for term, value in coordinate_conversion.domain_ancillaries().items():
                    if key == value:
                        coordinate_conversion.set_domain_ancillary(term, None)
                #--- End: for
                    
                ref.del_coordinate(key, None)
        #--- End: if

        return self._pop(key, None)
    #--- End: def

    def _set_construct(self, construct, key=None, axes=None,
                       copy=True):
        '''Set a metadata construct.

.. versionadded:: 1.7.0

.. seealso:: `_del_construct`, `_get_construct`,
             `_set_construct_data_axes`

:Parameters:

    construct:
        The metadata construct to be inserted.


    key: `str`, optional
        The construct identifier to be used for the construct. If not
        set then a new, unique identifier is created automatically. If
        the identifier already exisits then the exisiting construct
        will be replaced.

        *Parameter example:*
          ``key='cellmeasure0'``

    axes: (sequence of) `str`, optional
        The construct identifiers of the domain axis constructs
        spanned by the data array. An exception is raised if used for
        a metadata construct that can not have a data array,
        i.e. domain axis, cell method and coordinate reference
        constructs.

        The axes may also be set afterwards with the
        `set_construct_data_axes` method.

        *Parameter example:*
          ``axes='domainaxis1'``
        
        *Parameter example:*
          ``axes=['domainaxis1']``
        
        *Parameter example:*
          ``axes=('domainaxis1', 'domainaxis0')``
        
    copy: `bool`, optional
        If True then return a copy of the unique selected
        construct. By default the construct is not copied.

:Returns:

     `str`
        The construct identifier for the construct.
    
**Examples:**

>>> key = f.set_construct(c)
>>> key = f.set_construct(c, copy=False)
>>> key = f.set_construct(c, axes='domainaxis2')
>>> key = f.set_construct(c, key='cellmeasure0')

        '''
#    extra_axes: `int`, optional
#        The number of extra, trailing data array axes that do **not**
#        correspond to a domain axis specified by the *axes*
#        parameter. For example, a coordinate bounds data array may has
#        one or two extra axes. By default it assumed that there are no
#        extra axes.
#
#          *Parameter example:*
#             ``extra_axes=1``

#        construct_type = construct.construct_type
        construct_type = self._check_construct_type(construct.construct_type)
                                                
        if key is None:
            # Create a new construct identifier
            key = self.new_identifier(construct_type)
    
#        if construct_type in self._array_constructs:
#            #------------------------defaulrt=---------------------------------
#            # The construct could have a data array
#            #---------------------------------------------------------
#            if axes is None:
#                raise ValueError(
#"Can't set {} construct: Must specify the domain axes for the data array".format(
#    self._construct_type_description(construct_type)))
#            
#            if isinstance(axes, basestring):
#                axes = (axes,)
#            
##            domain_axes = self.constructs(construct='domain_axis')
#            domain_axes = self.select(construct='domain_axis')
#
#            axes_shape = []
#            for axis in axes:
#                if axis not in domain_axes:
#                    raise ValueError(                    
#"Can't set {!r}: Domain axis {!r} does not exist".format(
#    construct, axis))
#
#                axes_shape.append(domain_axes[axis].get_size())
#            #--- End: for
#            axes_shape = tuple(axes_shape)
#            extra_axes=0        
#            if (construct.has_data() and 
#                construct.data.shape[:construct.data.ndim - extra_axes] != axes_shape):
#                raise ValueError(
#                    "Can't set {!r}: Data array shape of {!r} does not match the shape required by domain axes {}: {}".format(
#    construct, construct.data.shape, tuple(axes), axes_shape))
#
#            self._set_construct_axes(key, axes)
#
#        elif axes is not None:
#            raise ValueError(
#"Can't set {!r}: Can't provide domain axis constructs for {} construct".format(
#    construct, self._construct_type_description(construct_type)))
#        #--- End: if


        if construct_type in self._array_constructs:
            #---------------------------------------------------------
            # The construct could have a data array
            #---------------------------------------------------------
            if axes is None:
                raise ValueError(
"Can't set {} construct: Must specify the domain axes for the data array".format(
    self._construct_type_description(construct_type)))

            self._set_construct_data_axes(key=key, axes=axes,
                                          construct=construct)
        elif axes is not None:
            raise ValueError(
"Can't set {!r}: Can't provide domain axis constructs for {} construct".format(
    construct, self._construct_type_description(construct_type)))

        # Record the construct type
        self._construct_type[key] = construct_type

        if copy:
            # Create a deep copy of the construct
            construct = construct.copy()

        # Insert the construct
        self._constructs[construct_type][key] = construct

        # Return the identifier of the construct
        return key
    #--- End: def

    def _set_construct_data_axes(self, key, axes, construct=None):
        '''<TODO>

.. versionadded:: 1.7.0

:Parameters:

    key: `str`, optional
        The construct identifier of metadata construct.

        *Parameter example:*
          ``key='cellmeasure0'``

    axes: (sequence of) `str`
        The construct identifiers of the domain axis constructs
        spanned by the data array. An exception is raised if used for
        a metadata construct that can not have a data array,
        i.e. domain axis, cell method and coordinate reference
        constructs.

        *Parameter example:*
          ``axes='domainaxis1'``

        *Parameter example:*
          ``axes=['domainaxis1']``

        *Parameter example:*
          ``axes=['domainaxis1', 'domainaxis0']``
        
:Returns:

    `None`

**Examples:**

>>> key = f.set_construct(c)
>>> f.set_construct_data_axes(key, axes='domainaxis1')

        '''
        if construct is None:
            if self.construct_type(key) is None:
                raise ValueError(
                    "Can't set axes for non-existent construct identifier {!r}".format(key))

            construct = self[key]        
        
        if isinstance(axes, basestring):
            axes = (axes,)
            
        domain_axes = self.type('domain_axis')
        
        axes_shape = []
        for axis in axes:
            if axis not in domain_axes:
                raise ValueError(                    
                    "Can't set {!r} domain axes: Domain axis {!r} does not exist".format(
                        construct, axis))

            axes_shape.append(domain_axes[axis].get_size())

        axes_shape = tuple(axes_shape)
        extra_axes=0        
        if (construct.has_data() and 
            construct.data.shape[:construct.data.ndim - extra_axes] != axes_shape):
            raise ValueError(
"Can't set {!r}: Data array shape of {!r} does not match the shape required by domain axes {}: {}".format(
    construct, construct.data.shape, tuple(axes), axes_shape))

        self._construct_axes[key] = tuple(axes)
    #--- End: def

    # ----------------------------------------------------------------
    # Dictionary-like methods    
    # ----------------------------------------------------------------
    def items(self):
        '''
        '''
        return self._dictionary().items()
    #--- End: def
    
    def keys(self):
        '''
        '''
        return self._construct_type.keys()
    #--- End: def
    
    def values(self):
        '''
        '''
        return self._dictionary().values()
    #--- End: def
    
    def construct_types(self):
        '''TODO
        '''
        out =  self._construct_type.copy()
        if self._ignore:
            for x in self._ignore:
                del out[x]

        return out
    #--- End: def

    def data_constructs(self, axes=None, copy=False):
        '''TODO
        '''
        out = {}

        if not self._ignore:
            for construct_type in self._array_constructs:
                out.update(self._constructs[construct_type])
        else:
            ignore = self._ignore
            for construct_type in self._array_constructs:
                if construct_type not in ignore:
                    out.update(self._constructs[construct_type])

        if axes:
            spans_axes = set(axes)
            constructs_data_axes = self.data_axes()
            for key, construct in list(out.items()):
                x = constructs_data_axes[key]
                if not spans_axes.intersection(x):
                    del out[key]
        #--- End: def

        return out
    #--- End: def
    
    def non_array_constructs(self):
        '''TODO
        '''
        out = {}        
        if not self._ignore:
            for construct_type in self._non_array_constructs:
                out.update(self._constructs[construct_type])
        else:
            ignore = self._ignore
            for construct_type in self._non_array_constructs:
                if construct_type not in ignore:
                    out.update(self._constructs[construct_type])

        return out
    #--- End: def

    def get(self, default=ValueError()):
        '''
        '''
        if not self:
            return self._default(default, "Can't get zero constructs")

        if len(self) > 1:
            return self._default(default,
                                 "Can't get {} constructs".format(len(self)))
        
        _, construct = self._dictionary().popitem()
            
        return construct
    #--- End: def

    def get_key(self, default=ValueError()):
        '''
        '''
        if not self:
            return self._default(default, "Can't get key for zero constructs")

        if len(self) > 1:
            return self._default(default,
                                 "Can't get key for {} constructs".format(len(self)))
        
        key, _ = self._dictionary().popitem()
            
        return key
    #--- End: def
        
#    def constructs(self, construct=None, copy=False):
#        '''Return metadata constructs
#
#Constructs are returned as values of a dictionary, keyed by their
#construct identifiers.
#
#.. versionadded:: 1.7.0
#
#.. seealso:: `del_construct`, `get_construct`, `set_construct`
#
#:Parameters:
#
#    construct_type: (sequence of) `str`, optional
#        Select constructs of the given type, or types. Valid types
#        are:
#
#          ==========================  ================================
#          *construct*                 Constructs
#          ==========================  ================================
#          ``'domain_ancillary'``      Domain ancillary constructs
#          ``'dimension_coordinate'``  Dimension coordinate constructs
#          ``'domain_axis'``           Domain axis constructs
#          ``'auxiliary_coordinate'``  Auxiliary coordinate constructs
#          ``'cell_measure'``          Cell measure constructs
#          ``'coordinate_reference'``  Coordinate reference constructs
#          ``'cell_method'``           Cell method constructs
#          ``'field_ancillary'``       Field ancillary constructs
#          ==========================  ================================
#
#        *Parameter example:*
#          ``construct='dimension_coordinate'``
#
#        *Parameter example:*
#          ``construct=['auxiliary_coordinate']``
#
#        *Parameter example:*
#          ``construct=['domain_ancillary', 'cell_method']``
#
#        Note that a domain never contains cell method nor field
#        ancillary constructs.
#
#    copy: `bool`, optional
#        If True then return copies of the constructs. By default the
#        constructs are not copied.
#
#:Returns:
#
#    `Constructs`
#        <TODO>
#
#**Examples:**
#
#>>> f.constructs()
#<TODO>
#
#        '''
#        return self.select(copy=copy)
#        out = self.view(ignore=self._ignore)
#                              
#        
#        if construct is not None:
#            if isinstance(construct, basestring):
#                construct = (construct,)
#        #--- End: if
#        
#        if construct is not None:
#            if construct == ('cell_method',):
#                out = self._constructs[construct[0]].copy()
#            else:                
#                out = {}
#                
#            for ct in construct:
#                ct = self._check_construct_type(ct)
#                out.update(self._constructs[ct])            
#        else:
#            out = {}
#            ignore = self._ignore
#            for key, value in self._constructs.items():
#                if key not in ignore:
#                    out.update(value)
#        #--- End: if
#
#        if copy:
#            for key, construct in list(out.items()):
#                out[key] = construct.copy()
#        #--- End: if
#
#        return out
    #--- End: def

#    def constructs_data_axes(self):
#        '''Return the domain axes spanned by metadata construct data arrays.
#
#.. versionadded:: 1.7.0
#
#.. seealso:: `constructs`, `get_construct_data_axes`
#
#:Returns:
#
#    `dict`
#        <TODO>
#        The identifiers of the domain axes constructs spanned by
#        metadata construct data arrays. If a metadata construct does
#        not have a data array then `None` is returned.
#
#**Examples:**
#
#>>> f.constructs_data_axes()
#<TODO>
#
#        '''
##        if cid is None:
#        # Return all of the constructs' axes
#        if not self._ignore:
#            return self._construct_axes.copy()
#        else:
#            ignore = self._ignore
#            out = {}
#            for construct_type, keys in self._constructs.items():
#                if construct_type not in ignore:
#                    for key in keys:
#                        _ = self._construct_axes.get(key)
#                        if _ is not None:
#                            out[key] = _
#            #--- End: for
#
#            return out
#        #--- End: if
        
#        # Return a particular construct's axes
#        if self._ignore and self.construct_type(cid) is None:
#            cid = None#
#
#        return self._construct_axes.get(cid)
    #--- End: def
    
    def data_axes(self):
        '''Return the domain axes spanned by all construct data arrays.

.. versionadded:: 1.7.0

.. seealso:: `get_construct_data_axes`, `select`

:Returns:

    `dict`
        <TODO>
        The identifiers of the domain axes constructs spanned by
        metadata construct data arrays. If a metadata construct does
        not have a data array then `None` is returned.

**Examples:**

>>> c.data_axes()
<TODO>

        '''
        if not self._ignore:
            return self._construct_axes.copy()
        else:
            ignore = self._ignore
            out = {}
            for construct_type, keys in self._constructs.items():
                if construct_type not in ignore:
                    for key in keys:
                        _ = self._construct_axes.get(key)
                        if _ is not None:
                            out[key] = _
            #--- End: for

            return out
    #--- End: def

    def copy(self, data=True):
        '''Return a deep copy.

``c.copy()`` is equivalent to ``copy.deepcopy(c)``.

:Returns:

    `Constructs`
        The copy.

**Examples:**

>>> d = c.copy()

        '''
        return type(self)(source=self, copy=True, _view=False,
                          _use_data=data, _ignore=self._ignore)
    #--- End: def

    def axes_to_constructs(self):
        '''TODO

:Returns:

    `dict`

**Examples:**

>>> print c.axes_to_constructs()
{('domainaxis1',): {
        'auxiliary_coordinate': {'auxiliary_coordinate2': <AuxiliaryCoordinate: greek_letters(10) >},
        'field_ancillary'     : {'fieldancillary2': <FieldAncillary: ncvar%ancillary_data_2(10) >},
        'domain_ancillary'    : {}, 
        'cell_measure'        : {}, 
        'dimension_coordinate': {'dimensioncoordinate1': <DimensionCoordinate: grid_latitude(10) degrees>}
        },
('domainaxis1', 'domainaxis2'): {
        'auxiliary_coordinate': {'auxiliary_coordinate0': <AuxiliaryCoordinate: latitude(10, 9) degree_N>},
        'field_ancillary'     : {'fieldancillary0': <FieldAncillary: ncvar%ancillary_data(10, 9) >},
        'domain_ancillary'    : {'domainancillary2': <DomainAncillary: surface_altitude(10, 9) m>},
        'cell_measure'        : {},
        'dimension_coordinate': {}
        },
('domainaxis2', 'domainaxis1'): {
        'auxiliary_coordinate': {'auxiliary_coordinate1': <AuxiliaryCoordinate: longitude(9, 10) degreeE>},
        'field_ancillary'     : {},
        'domain_ancillary'    : {},
        'cell_measure'        : {'cell_measure0': <CellMeasure: area(9, 10) km2>},
        'dimension_coordinate': {}
        },
('domainaxis0',): {
        'auxiliary_coordinate': {},
        'field_ancillary'     : {},
        'domain_ancillary'    : {'domainancillary1': <DomainAncillary: ncvar%b(1) >, 'domainancillary0': <DomainAncillary: ncvar%a(1) m>},
        'cell_measure'        : {},
        'dimension_coordinate': {'dimensioncoordinate0': <DimensionCoordinate: atmosphere_hybrid_height_coordinate(1) >}
        },
('domainaxis2',): {
        'auxiliary_coordinate': {},
        'field_ancillary'     : {'fieldancillary1': <FieldAncillary: ncvar%ancillary_data_1(9) >},
        'domain_ancillary'    : {},
        'cell_measure'        : {},
        'dimension_coordinate': {'dimensioncoordinate2': <DimensionCoordinate: grid_longitude(9) degrees>}
        }
}

'''
        out = {}


        data_axes = self.data_axes()
        
        for axes in data_axes.values():
            d = {construct_type: {}
                 for construct_type in self._array_constructs}

            out[axes] = d
        #--- End: for

        for cid, construct in self.data_constructs().items():
            axes = data_axes.get(cid)
            construct_type = self._construct_type[cid]
            out[axes][construct_type][cid] = construct

        return out
    #--- End: def

#    def get_construct(self, key):
#        '''Return a metadata construct.
#
#.. versionadded:: 1.7.0
#
#.. seealso:: `del_construct`, `select`, `set_construct`
#
#:Parameters:
#
#    key: `str`
#        The identifier of the metadata construct.
#
#        *Parameter example:*
#          ``key='domainaxis1'``
#
#:Returns:
#
#        The metadata construct.
#
#**Examples:**
#
#>>> f.constructs()
#{'auxiliarycoordinate0': <AuxiliaryCoordinate: latitude(10, 9) degree_N>,
# 'auxiliarycoordinate1': <AuxiliaryCoordinate: longitude(9, 10) degreeE>,
# 'auxiliarycoordinate2': <AuxiliaryCoordinate: long_name:greek_letters(10) >,
# 'cellmethod0': <CellMethod: domainaxis2: mean (interval: 1 day comment: ok)>,
# 'coordinatereference1': <CoordinateReference: rotated_latitude_longitude>,
# 'dimensioncoordinate1': <DimensionCoordinate: grid_latitude(10) degrees>,
# 'dimensioncoordinate2': <DimensionCoordinate: grid_longitude(9) degrees>,
# 'domainaxis1': <DomainAxis: 10>,
# 'domainaxis2': <DomainAxis: 9>}
#>>> f.get_construct('dimensioncoordinate1')
#<DimensionCoordinate: grid_latitude(10) degrees>
#
#        '''
#        construct_type = self.construct_type(key)
#        if construct_type is None:
#            raise ValueError('No metadata construct found')
#            
#        d = self._constructs.get(construct_type)
#        if d is None:
#            d = {}
#            
#        try:            
#            return d[key]
#        except KeyError:
#            raise ValueError('No metadata construct found')
#    #--- End: def
    
#    def has_construct(self, key):
#        '''Whether a construct exists.
#
#.. versionadded:: 1.7.0
#
#.. seealso:: `constructs`, `del_construct`, `get_construct`,
#             `set_construct`
#
#:Parameters:
#
#    key: `str`
#        The identifier of the metadata construct.
#
#        *Parameter example:*
#          ``key='cellmeasure1'``
#
#:Returns:
#
#    `bool`
#        True if the metadata construct exists, otherwise False.
#
#**Examples:**
#
#>>> f.constructs()
#{'auxiliarycoordinate0': <AuxiliaryCoordinate: latitude(10, 9) degree_N>,
# 'auxiliarycoordinate1': <AuxiliaryCoordinate: longitude(9, 10) degreeE>,
# 'auxiliarycoordinate2': <AuxiliaryCoordinate: long_name:greek_letters(10) >,
# 'coordinatereference1': <CoordinateReference: rotated_latitude_longitude>,
# 'dimensioncoordinate1': <DimensionCoordinate: grid_latitude(10) degrees>,
# 'dimensioncoordinate2': <DimensionCoordinate: grid_longitude(9) degrees>,
# 'domainaxis1': <DomainAxis: 10>,
# 'domainaxis2': <DomainAxis: 9>}
#>>> f.has_construct('dimensioncoordinate1')
#True
#>>> f.has_construct('domainaxis99')
#False
#
#        '''
#        try:
#            self.get_construct(key)
#        except ValueError:
#            return False
#        else:
#            return True        
#    #--- End: def

    def new_identifier(self, construct_type):
        '''Return a new, unique identifier for a construct.

.. versionadded:: 1.7.0

:Parameters:

    construct_type: `str`

:Returns:

    `str`
        The new identifier.

**Examples:**

>>> d.items().keys()
['aux2', 'aux0', 'dim1', 'ref2']
>>> d.new_identifier('aux')
'aux3'
>>> d.new_identifier('ref')
'ref1'

>>> d.items().keys()
[]
>>> d.new_identifier('dim')
'dim0'

>>> d.axes()
{'dim0', 'dim4'}
>>> d.new_identifier('axis')
'dim2'

>>> d.axes()
{}
>>> d.new_identifier('axis')
'dim0'

        '''
        keys = self._constructs[construct_type]

        key_base = self._key_base[construct_type]
        key = '{0}{1}'.format(key_base, len(keys))
        while key in keys:
            n += 1
            key = '{0}{1}'.format(key_base, n)

        return key
    #--- End: def

    def replace(self, key, construct, axes=None, copy=True):
        '''<TODO>

.. note:: No checks on the axes are done!!!!!
'''
        construct_type = self.construct_types().get(key)
        if construct_type is None:
            raise ValueError("Can't replace non-existent construct {!r}".format(key))

        if axes is not None and construct_type in self._array_constructs:        
            self._construct_axes[key] = tuple(axes)

        if copy:
            construct = construct.copy()
            
        self._constructs[construct_type][key] = construct
    #--- End: def

    def ordered(self):
        '''<TODO>

.. versionadded:: 1.7.0

:Returns:

     `Constructs`
         <TODO>

**Examples:**

<TODO>

        '''
        if len(self._ordered_constructs) > 1:
            raise ValueError(" can't get order multiple types .......")
    
        if self._ordered_constructs != set(self._constructs):
            raise ValueError(" can't order un-orderable types .......")        

        return OrderedDict(self._constructs[tuple(self._ordered_constructs)[0]])
    #--- End: def
    
#    def select(self, construct=None):
#        '''Select metadata constructs.
#
#By default all metadata constructs are selected, but a subset may be
#chosen via the optional parameters. If multiple parameters are
#specified, then the constructs that satisfy *all* of the criteria are
#returned.
#
#.. versionadded:: 1.7.0
#
#.. seealso:: `get`, `items`, `keys`, `values`
#
#:Parameters:
#
#    construct: (sequence of) `str`, optional
#        Select constructs of the given type, or types. Valid types
#        are:
#
#          ==========================  ================================
#          *construct*                 Constructs
#          ==========================  ================================
#          ``'domain_ancillary'``      Domain ancillary constructs
#          ``'dimension_coordinate'``  Dimension coordinate constructs
#          ``'domain_axis'``           Domain axis constructs
#          ``'auxiliary_coordinate'``  Auxiliary coordinate constructs
#          ``'cell_measure'``          Cell measure constructs
#          ``'coordinate_reference'``  Coordinate reference constructs
#          ``'cell_method'``           Cell method constructs
#          ``'field_ancillary'``       Field ancillary constructs
#          ==========================  ================================
#
#        *Parameter example:*
#          ``construct='dimension_coordinate'``
#
#        *Parameter example:*
#          ``construct=['auxiliary_coordinate']``
#
#        *Parameter example:*
#          ``construct=['domain_ancillary', 'cell_method']``
#
#        Note that a domain can never contain cell method nor field
#        ancillary constructs.
#
#:Returns:
#
#     `Constructs`
#         <TODO>
#
#**Examples:**
#
#<TODO>
#
#        '''
#        
#        if construct is not None and isinstance(construct, basestring):
#            construct = (construct,)
#
#        if construct:
#            # Ignore the all but the requested construct types
#            ignore = set(self._key_base)
#            ignore.difference_update(set(construct))
#        else:
#            # Keep all construct types
#            ignore = self._ignore
#
#        return type(self)(source=self, _ignore=ignore, _view=False, copy=False)
#    #--- End: def

    def type(self,*types):
        '''Select metadata constructs.

By default all metadata constructs are selected, but a subset may be
chosen via the optional parameters. If multiple parameters are
specified, then the constructs that satisfy *all* of the criteria are
returned.

.. versionadded:: 1.7.0

.. seealso:: `get`, `items`, `keys`, `values`

:Parameters:

    construct: (sequence of) `str`, optional
        Select constructs of the given type, or types. Valid types
        are:

          ==========================  ================================
          *construct*                 Constructs
          ==========================  ================================
          ``'domain_ancillary'``      Domain ancillary constructs
          ``'dimension_coordinate'``  Dimension coordinate constructs
          ``'domain_axis'``           Domain axis constructs
          ``'auxiliary_coordinate'``  Auxiliary coordinate constructs
          ``'cell_measure'``          Cell measure constructs
          ``'coordinate_reference'``  Coordinate reference constructs
          ``'cell_method'``           Cell method constructs
          ``'field_ancillary'``       Field ancillary constructs
          ==========================  ================================

        *Parameter example:*
          ``construct='dimension_coordinate'``

        *Parameter example:*
          ``construct=['auxiliary_coordinate']``

        *Parameter example:*
          ``construct=['domain_ancillary', 'cell_method']``

        Note that a domain can never contain cell method nor field
        ancillary constructs.

:Returns:

     `Constructs`
         <TODO>

**Examples:**

<TODO>

        '''
        
#        if construct is not None and isinstance(construct, basestring):
#            construct = (construct,)

        if types:
            # Ignore the all but the requested construct types
            ignore = set(self._key_base)
            ignore.difference_update(set(types))
        else:
            # Keep all construct types
            ignore = self._ignore

        return self.shallow_copy(_ignore=ignore)
#        return type(self)(source=self, _ignore=ignore, _view=False, copy=False)
    #--- End: def

    def shallow_copy(self, _ignore=None):
        '''
        '''
        if _ignore is None:
            _ignore = self._ignore
            
        return type(self)(source=self, copy=False, _ignore=_ignore,
                          _view=False)
    #--- End: def

    def view(self, ignore=()):
        '''<TODO>

:Parameters:

    ignore: `bool`, optional

:Returns:

    `Constructs`
        <TODO>

**Examples:**

<TODO>
        '''
        return type(self)(source=self, _view=True, _ignore=ignore)
    #--- End: def
    
#--- End: class
