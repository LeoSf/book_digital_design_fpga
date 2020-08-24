/* ----------------------------------------------------------------------------------
 * Company:             None
 * Engineer:            Leandro D. Medus
 *
 * Create Date:         18:17:00 05/04/2020 (mm/dd/yyyy)
 * Design Name:         Abacus
 * Module Name:         top - Behavioral
 * Project Name:        < >
 * Target Devices:      Basys 3
 * Tool versions:       Vivado 2019.1
 * Description:
 *
 * Dependencies:
 *
 *
 * Revision History:
 *      05/04/2020  v0.01 File created
 *
 * Additional Comments:
 *
 * ------------------------------------------------------------------------------- */

module module
(
    /* inputs */
    input           clk,        /* system clock                 */
    input           rst_n,      /* global reset - active low    */
    input [2:0]     in1,        /* first operand input          */
    input [2:0]     in2,        /* second operand input         */
    input [1:0]     sel,        /* operand selector             */
    /* outputs */
    output          overflow,   /* overflow flag                */
    output [5:0]    out_reg     /* result operand               */
);



endmodule
