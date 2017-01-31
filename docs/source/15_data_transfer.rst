*******************************
Data Transfer
*******************************

.. contents:: Table of Contents
   :depth: 2
   
Introduction
==================

MMIO
======
MMIO can be used to map PL memory to allow data to be read/written from Python. This is a simple way to transfer data, and is most appropriate for small amounts of data, as the performance will be relatively slow. Each MMIO read or write command will transfer 32 bits of data. 

The following examples sets up the MMIO to access memory location 0x40000000 - 0x40001000.

The value 0xdeadbeef is sent to location ADDRESS_OFFSET. ADDRESS_OFFSET is 0x10, and this is offset from the start of the MMIO area 0x40000000. This means 0xdeadbeef will be written to 0x40000010. Finally the same location is read, and the result stored in result. This assumes the memory area defined for the MMIO, 0x40000000 - 0x40001000, is accessible to the PS. 

.. code-block:: Python

   from pynq import MMIO
   ACCELERATOR_ADDRESS 0x40000000
   MEMORY_SIZE = 0x1000
   ADDRESS_OFFSET = 0x10
   
   mmio = MMIO(ACCELERATOR_ADDRESS,MEMORY_SIZE) 

   data = 0xdeadbeef
   self.mmio.write(ADDRESS_OFFSET, data)
   result = self.mmio.read(ADDRESS_OFFSET)



