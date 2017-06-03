#ifndef __PMOD_JSTK2_
#define __PMOD_JSTK2_

#include "pmod.h"
#include "pmod_io_switch.h"

// Mailbox commands (interactions between c and python programs)
#define READ_X   0x3
#define READ_Y   0x4
#define READ_XY  0x5
#define READ_BTN 0x6
#define LED_ON   0x7
#define LED_OFF  0x8

// JSTK2 commands (interactions between c program and joystick)
#define getData   0xC0
#define setLedOff 0x80
#define setLedOn  0x81
#define setLedRGB 0x84

typedef struct sample {
	u16 x   = 0;
	//u8 x   = 0;
	u16 y   = 0;
	//u8 y   = 0;
	u8 btn = 0; // button state
	//u8 led = 0; // LED state
	u8 r   = 255; // LED color settings
	u8 g   = 0;
	u8 b   = 0;
} sample_pkt;

/*
typedef struct calibrate {
	u8 x_off;
	u8 y_off;
} csettings;
*/

#endif