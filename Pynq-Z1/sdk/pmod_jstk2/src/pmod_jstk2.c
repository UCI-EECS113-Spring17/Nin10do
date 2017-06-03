#include "pmod_jstk2.h"

int main(void) {
	u32        cmd;
	sample_pkt current; // contains x, y, btn, rgb values
	// jstk2 transfers 5 bytes with it's standard packet,
	// and 6 or 7 with the extended packet, based off the command
	int length = 5;
	int extlen = 7;
	int i      = 0;
	// read buffer, 1 byte at a time
	u8 rb[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
	// write buffer, 1 byte at a time
	u8 wb[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; 
	
	// Initialize PMOD device and configure switch
	pmod_init(0, 1);
	config_pmod_switch(SS, MOSI, MISO, SCLK, GPIO_4, GPIO_5, GPIO_6, GPIO_7);
	/************************************
	***** PMOD SWITCH CONFIGURATION *****
	* - Pin 0: Source selec, 0xd        *
	* - Pin 1: Master-Out Slave-in, 0xc *
	* - Pin 2: Master-in Slave-out, 0xb *
	* - Pin 3: SPI Clk, 0xa             *
	* - Pin 4: GPIO_4, 0x4 (unused)     *
	* - Pin 5: GPIO_5, 0x5 (unused)     *
	* - Pin 6: GPIO_6, 0x6 (unused)     *
	* - Pin 7: GPIO_7, 0x7 (unused)     *
	************************************/
	
	while (1) {
		while ((MAILBOX_CMD_ADDR & 0x01) == 0); // wait for a command
		cmd = MAILBOX_CMD_ADDR;
		
		// Update current info
		if (!(cmd == LED_ON || cmd == LED_OFF)) {
			wb[0] = getData;
			wb[1] = 0; // ignored
			wb[2] = 0;
			wb[3] = 0;
			wb[4] = 0;
			wb[5] = 0;
			wb[6] = 0;
			spi_transfer(SPI_BASEADDR, length, rb, wb); // TODO: rework segment
			/**************************************
			* 5-byte transfer protocol for JSTK2: *
			* - MOSI:                             *
			*   1) command                        *
			*   2) param1                         *
			*   3) param2                         *
			*   4) param3                         *
			*   5) param4                         *
			* - MISO:                             *
			*   1) smpX (low)                     *
 			*   2) smpX (high)                    *
			*   3) smpY (low)                     *
			*   4) smpY (high)                    *
			*   5) fsButtons:                     *
			*   bit 0 = joystick press btn state  *
			*   bit 1 = trigger button state      *
			*   bits 2-6 are ignored              *
			*   bit 7 = extpkt, 1 if there's      *
			*      additional data after byte 5   *
			**************************************/
			//current->x   = ((rb[1] << 8) | rb[0]); // bitshift high byte, or with low byte to get 16-bit data
			//current->y   = ((rb[3] << 8) | rb[2]);
			current->x = rb[5];
			current->y = rb[6];
			current->btn = ((rb[4] >> 1) & 0x01); // bit 1 from byte 5; 1 if button pressed, 0 otherwise 
		} else if (cmd == LED_ON) {
			//current->led = 1;
			// Read in rgb data
			//if (!MAILBOX_DATA(0) && !MAILBOX_DATA(1) && !MAILBOX_DATA(2)) {
			//	if (!current->r && !current->g && !current->b) {
					// Restore default color (red)
			//		current->r = 255;
			//	}
				// Otherwise keep current color
			//	break;
			//}
			current->r = MAILBOX_DATA(0);
			current->g = MAILBOX_DATA(1);
			current->b = MAILBOX_DATA(2);
			
		}// else if (cmd == LED_OFF) {
			//current->led = 0; // This variable can probably be removed
		//}
	
		switch (cmd) {
			// Write x position
			case READ_X:
				MAILBOX_DATA(0) = current->x;
				MAILBOX_CMD_ADDR = 0x0; // Signals done
				break;
				
			// Write y position
			case READ_Y:
				MAILBOX_DATA(0) = current->y;
				MAILBOX_CMD_ADDR = 0x0;
				break;
			
			// Write both x and y positions
			case READ_XY:
				MAILBOX_DATA(0) = current->x;
				MAILBOX_DATA(1) = current->y;
				MAILBOX_CMD_ADDR = 0x0;
				break;
			
			// Write current button state
			case READ_BTN:
				MAILBOX_DATA(0) = current->btn;
				MAILBOX_CMD_ADDR = 0x0;
				break;
			
			// Read rgb data and turn on LED
			case LED_ON:
				wb[0] = setLedRGB;
				wb[1] = current->r;
				wb[2] = current->g;
				wb[3] = current->b;
				wb[4] = 0; // ignored
				spi_transfer(SPI_BASEADDR, length, 0, wb);
				MAILBOX_CMD_ADDR = 0x0;
				break;
				
			// Turn off LED
			case LED_OFF: // TODO
				wb[0] = setLedOff;
				wb[1] = 0; // ignored
				wb[2] = 0;
				wb[3] = 0;
				wb[4] = 0;
				spi_transfer(SPI_BASEADDR, length, 0, wb);
				MAILBOX_CMD_ADDR = 0x0;
				break;
			
			default:
				// Unrecognized command
				MAILBOX_CMD_ADDR = 0x0;
				break;
		}
	}
	
	return 0;
}

/*****
void spi_transfer(u32 BaseAddress, int bytecount, u8* readBuffer, u8* writeBuffer):
 - macro SPI_BASEADDR is defined in pmod.h
 - Write contents of writebuffer to reg, delays for ~100 ns, then reads from data receive reg and writes it to readbuffer
 - XSpi_ReadReg(addr, offest) returns content of 'addr'+'offset'
 - XSpi_WriteReg(addr, offset, contents) writes 'contents' to 'addr'+'offset'
 
Macros from xspi_l.h:
 - XSP_SR_OFFSET		0x64	< Status Register 
 - XSP_SRR_OFFSET		0x40	< Software Reset register 
 - XSP_DTR_OFFSET		0x68	< Data transmit
 - XSP_DRR_OFFSET		0x6C	< Data receive




*****/