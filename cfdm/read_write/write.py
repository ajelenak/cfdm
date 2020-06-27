from ..cfdmimplementation import implementation

from .netcdf import NetCDFWrite


_implementation = implementation()


def write(fields, filename, fmt='NETCDF4', overwrite=True,
          global_attributes=None, variable_attributes=None,
          file_descriptors=None, external=None, Conventions=None,
          datatype=None, least_significant_digit=None,
          endian='native', compress=0, fletcher32=False, shuffle=True,
          string=True, verbose=None, warn_valid=True, group=True,
          _implementation=_implementation):
    '''Write field constructs to a netCDF file.

    **File format**

    See the *fmt* parameter for details on which output netCDF file
    formats are supported.

    **NetCDF variable and dimension names**

    These names are stored within constructs read a from dataset, or
    may be set manually. They are used when writing a field construct
    to the file. If a name has not been set then one will be
    constructed (usually based on the standard name if it exists). The
    names may be modified internally to prevent duplication in the
    file.

    Each construct, or construct component, that corresponds to a
    netCDF variable has the following methods to get, set and remove a
    netCDF variable name: `!nc_get_variable`, `!nc_set_variable` and
    `!nc_del_variable` method

    The domain axis construct has the following methods to get, set
    and remove a netCDF dimension name:
    `~cfdm.DomainAxis.nc_get_dimension`,
    `~cfdm.DomainAxis.nc_set_dimension` and
    `~cfdm.DomainAxis.nc_del_dimension`.

    **NetCDF attributes**

    Field construct properties may be written as netCDF global
    attributes and/or netCDF data variable attributes. See the
    *file_descriptors*, *global_attributes* and *variable_attributes*
    parameters for details.

    **External variables**

    Metadata constructs marked as external are omitted from the file
    and referred to via the netCDF ``external_variables`` global
    attribute. However, omitted constructs may be written to an
    external file (see the *external* parameter for details).

    **NetCDF unlimited dimensions**

    Domain axis constructs that correspond to NetCDF unlimited
    dimensions may be accessed with the
    `~cfdm.DomainAxis.nc_is_unlimited` and
    `~cfdm.DomainAxis.nc_set_unlimited` methods of a domain axis
    construct.
    

    **NetCDF hierarchical groups**
    
    Hierarchical groups in CF provide a mechanism to structure
    variables within netCDF4 datasets with well defined rules for
    resolving references to out-of-group netCDF variables and
    dimensions. The group structure defined by a field construct's
    netCDF interface will, by default, be recreated in the output
    dataset. See the *group* parameter for details.


    **NetCDF4 HDF chunk sizes**

    HDF5 chunksizes may be set on construct's data. See the
    `~cfdm.Data.nc_hdf5_chunksizes`,
    `~cfdm.Data.nc_clear_hdf5_chunksizes` and
    `~cfdm.Data.nc_set_hdf5_chunksizes` metods of a `Data` instance.

    .. versionadded:: 1.7.0

    .. seealso:: `read`

    :Parameters:

        fields: (sequence of) `Field`
            The field constructs to write to the file.

        filename: `str`
            The output netCDF file name. Various type of expansion are
            applied to the file names.

            Relative paths are allowed, and standard tilde and shell
            parameter expansions are applied to the string.

            *Parameter example:*
              The file ``file.nc`` in the user's home directory could
              be described by any of the following:
              ``'$HOME/file.nc'``, ``'${HOME}/file.nc'``,
              ``'~/file.nc'``, ``'~/tmp/../file.nc'``.

        fmt: `str`, optional
            The format of the output file. One of:

            ==========================  ================================
            *fmt*                       Output file type
            ==========================  ================================
            ``'NETCDF4'``               NetCDF4 format file. This is the
                                        default.

            ``'NETCDF4_CLASSIC'``       NetCDF4 classic format file (see
                                        below)

            ``'NETCDF3_CLASSIC'``       NetCDF3 classic format file
                                        (limited to file sizes less
                                        than 2GB).

            ``'NETCDF3_64BIT_OFFSET'``  NetCDF3 64-bit offset format
                                        file

            ``'NETCDF3_64BIT'``         An alias for
                                        ``'NETCDF3_64BIT_OFFSET'``

            ``'NETCDF3_64BIT_DATA'``    NetCDF3 64-bit offset format
                                        file with extensions (see below)
            ==========================  ================================

            By default the format is ``'NETCDF4'``.

            All formats support large files (i.e. those greater than
            2GB) except ``'NETCDF3_CLASSIC'``.

            ``'NETCDF3_64BIT_DATA'`` is a format that requires version
            4.4.0 or newer of the C library (use `cfdm.environment` to
            see which version if the netCDF-C library is in use). It
            extends the ``'NETCDF3_64BIT_OFFSET'`` binary format to
            allow for unsigned 64 bit integer data types and 64-bit
            dimension sizes.

            ``'NETCDF4_CLASSIC'`` files use the version 4 disk format
            (HDF5), but omits features not found in the version 3
            API. They can be read by HDF5 clients. They can also be
            read by netCDF3 clients only if they have been re-linked
            against the netCDF4 library.

            ``'NETCDF4'`` files use the version 4 disk format (HDF5)
            and use the new features of the version 4 API.

        overwrite: `bool`, optional
            If False then raise an error if the output file
            pre-exists. By default a pre-existing output file is
            overwritten.

        Conventions: (sequence of) `str`, optional
             Specify conventions to be recorded by the netCDF global
             ``Conventions`` attribute. By default the current
             conventions are always included, but if an older CF
             conventions is defined then this is used instead.

             *Parameter example:*
               ``Conventions='UGRID-1.0'``

             *Parameter example:*
               ``Conventions=['UGRID-1.0']``

             *Parameter example:*
               ``Conventions=['CMIP-6.2', 'UGRID-1.0']``

             *Parameter example:*
               ``Conventions='CF-1.7'``

             *Parameter example:*
               ``Conventions=['CF-1.7', 'UGRID-1.0']``

             Note that if the ``Conventions`` property is set on a
             field construct then it is ignored.

        file_descriptors: `dict`, optional
             Create description of file contents netCDF global
             attributes from the specified attributes and their
             values.

             If any field construct has a property with the same name
             then it will be written as a netCDF data variable
             attribute, even if it has been specified by the
             *global_attributes* parameter, or has been flagged as
             global on any of the field constructs (see
             `cfdm.Field.nc_global_attributes` for details).

             Identification of the conventions being adhered to by the
             file are not specified as a file descriptor, but by the
             *Conventions* parameter instead.

             *Parameter example:*
               ``file_attributes={'title': 'my data'}``

             *Parameter example:*
               ``file_attributes={'history': 'created 2019-01-01',
               'foo': 'bar'}``

        global_attributes: (sequence of) `str`, optional
             Create netCDF global attributes from the specified field
             construct properties, rather than netCDF data variable
             attributes.

             These attributes are in addition to the following field
             construct properties, which are created as netCDF global
             attributes by default:

             * the description of file contents properties (as defined
               by the CF conventions), and

             * properties flagged as global on any of the field
               constructs being written (see
               `cfdm.Field.nc_global_attributes` for details).

             Note that it is not possible to create a netCDF global
             attribute from a property that has different values for
             different field constructs being written. In this case
             the property will not be written as a netCDF global
             attribute, even if it has been specified by the
             *global_attributes* parameter or is one of the default
             properties, but will appear as an attribute on the netCDF
             data variable corresponding to each field construct that
             contains the property.

             Any global attributes that are also specified as file
             descriptors will not be written as netCDF global
             variables, but as netCDF data variable attributes
             instead.

             *Parameter example:*
               ``global_attributes='project'``

             *Parameter example:*
               ``global_attributes=['project']``

             *Parameter example:*
               ``global_attributes=['project', 'experiment']``

        variable_attributes: (sequence of) `str`, optional
             Create netCDF data variable attributes from the specified
             field construct properties.

             By default, all field construct properties that are not
             created as netCDF global properties are created as
             attributes netCDF data variables. See the
             *global_attributes* parameter for details.

             Any field construct property named by the
             *variable_attributes* parameter will always be created as
             a netCDF data variable attribute

             *Parameter example:*
               ``variable_attributes='project'``

             *Parameter example:*
               ``variable_attributes=['project']``

             *Parameter example:*
               ``variable_attributes=['project', 'doi']``

        external: `str`, optional
            Write metadata constructs that have data and are marked as
            external to the named external file. Ignored if there are
            no such constructs.

        datatype: `dict`, optional
            Specify data type conversions to be applied prior to
            writing data to disk. This may be useful as a means of
            packing, or because the output format does not support a
            particular data type (for example, netCDF3 classic files
            do not support 64-bit integers). By default, input data
            types are preserved. Any data type conversion is only
            applied to the arrays on disk, and not to the input field
            constructs themselves.

            Data types conversions are defined by `numpy.dtype`
            objects in a dictionary whose keys are input data types
            with values of output data types.

            *Parameter example:*
              To convert 64-bit integers to 32-bit integers:
              ``datatype={numpy.dtype('int64'):
              numpy.dtype('int32')}``.

        endian: `str`, optional
            The endian-ness of the output file. Valid values are
            ``'little'``, ``'big'`` or ``'native'``. By default the
            output is native endian. See the `netCDF4 package
            <http://unidata.github.io/netcdf4-python>`_ for more
            details.

            *Parameter example:*
              ``endian='big'``

        compress: `int`, optional
            Regulate the speed and efficiency of compression. Must be
            an integer between ``0`` and ``9``. ``0`` means no
            compression; ``1`` is the fastest, but has the lowest
            compression ratio; ``9`` is the slowest but best
            compression ratio. The default value is ``0``. An error is
            raised if compression is requested for a netCDF3 output
            file format. See the `netCDF4 package
            <http://unidata.github.io/netcdf4-python>`_ for more
            details.

            *Parameter example:*
              ``compress=4``

        least_significant_digit: `int`, optional
            Truncate the input field construct data arrays, but not
            the data arrays of metadata constructs. For a given
            positive integer, N the precision that is retained in the
            compressed data is 10 to the power -N. For example, a
            value of 2 will retain a precision of 0.01. In conjunction
            with the *compress* parameter this produces 'lossy', but
            significantly more efficient, compression. See the
            `netCDF4 package
            <http://unidata.github.io/netcdf4-python>`_ for more
            details.

            *Parameter example:*
              ``least_significant_digit=3``

        fletcher32: `bool`, optional
            If True then the Fletcher-32 HDF5 checksum algorithm is
            activated to detect compression errors. Ignored if
            *compress* is ``0``. See the `netCDF4 package
            <http://unidata.github.io/netcdf4-python>`_ for details.

        shuffle: `bool`, optional
            If True (the default) then the HDF5 shuffle filter (which
            de-interlaces a block of data before compression by
            reordering the bytes by storing the first byte of all of a
            variable's values in the chunk contiguously, followed by
            all the second bytes, and so on) is turned off. By default
            the filter is applied because if the data array values are
            not all wildly different, using the filter can make the
            data more easily compressible.  Ignored if the *compress*
            parameter is ``0`` (which is its default value). See the
            `netCDF4 package
            <http://unidata.github.io/netcdf4-python>`_ for more
            details.

       string: `bool`, optional
           By default string-valued construct data are written as
           netCDF arrays of type string if the output file format is
           ``'NETCDF4'``, or of type char with an extra dimension
           denoting the maximum string length for any other output
           file format (see the *fmt* parameter). If *string* is False
           then string-valued construct data are written as netCDF
           arrays of type char with an extra dimension denoting the
           maximum string length, regardless of the selected output
           file format.

        verbose: `int` or `None`, optional
            If an integer from ``0`` to ``3``, corresponding to increasing
            verbosity (else ``-1`` as a special case of maximal and extreme
            verbosity), set for the duration of the method call (only) as
            the minimum severity level cut-off of displayed log messages,
            regardless of the global configured `cfdm.LOG_LEVEL`.

            Else, if `None` (the default value), log messages will be
            filtered out, or otherwise, according to the value of the
            `cfdm.LOG_LEVEL` setting.

            Overall, the higher a non-negative integer that is set (up to
            a maximum of ``3``) the more description that is printed to
            convey how constructs map to output netCDF dimensions, variables
            and attributes.

       warn_valid: `bool`, optional
            If False then do not print a warning when writing
            "out-of-range" data, as indicated by the values, if
            present, of any of the ``valid_min``, ``valid_max`` or
            ``valid_range`` properties on field and metadata
            constructs that have data. By default a warning is printed
            if any such construct has any of these properties in
            combination with out-of-range data.

            The consequence of writing out-of-range data values is
            that, by default, these values will be masked when the
            file is subsequently read.

            *Parameter example:*
              If a construct has ``valid_max`` property with value
              ``100`` and data with maximum value ``999``, then the
              resulting warning may be suppressed by setting
              ``warn_valid=False``.

            .. versionadded:: 1.8.3

        group: `bool`, optional
            If False then create a "flat" netCDF file, i.e. one with
            only the root group, regardless of any group structure
            specified by the field constructs. By default any groups
            defined by the netCDF interface of the field constucts and
            its components will be created and populated.

            .. versionadded:: 1.8.6

        _implementation: (subclass of) `CFDMImplementation`, optional
            Define the CF data model implementation that defines field
            and metadata constructs and their components.

    :Returns:

        `None`

    **Examples:**

    >>> cfdm.write(f, 'file.nc')

    >>> cfdm.write(f, 'file.nc', fmt='NETCDF3_CLASSIC')

    >>> cfdm.write(f, 'file.nc', external='cell_measures.nc')

    >>> cfdm.write(f, 'file.nc', Conventions='CMIP-6.2')

    '''
    # ----------------------------------------------------------------
    # Initialise the netCDF write object
    # ----------------------------------------------------------------
    netcdf = NetCDFWrite(_implementation)

    if fields:
        netcdf.write(fields, filename, fmt=fmt, overwrite=overwrite,
                     global_attributes=global_attributes,
                     variable_attributes=variable_attributes,
                     file_descriptors=file_descriptors,
                     external=external, Conventions=Conventions,
                     datatype=datatype,
                     least_significant_digit=least_significant_digit,
                     endian=endian, compress=compress,
                     shuffle=shuffle, fletcher32=fletcher32,
                     string=string, verbose=verbose,
                     warn_valid=warn_valid, group=group,
                     extra_write_vars=None)
