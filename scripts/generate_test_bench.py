# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Biong. Leandro D. Medus
Ph.D Student GPDD - ETSE
Universitat de València
leandro.d.medus@uv.es

11-05-2020

Script Description:
-------------------
This is a Script to generate a testbench automatically from a custom VHDL module.

Version: 1.7
------------

TODO:
    -- fail to detect: port   : out integer range 0 to 8);
this happen when appear as the las port in the entity followed by ");"

"""

import re
import sys

# prefix for the new generated file
testbench_prefix = "tb_"

# regex to split files names and absolute or relative paths
regex_path = re.compile(r'([\w|\\|//|\:|.]*[\\|//])*(\w*)(.vhd)', re.I)

# capture all the header description from the source file
regex_header = re.compile(r'(--.*)', re.I)

# regex for libraries
regex_libraries = re.compile(r'(library\s\w*;| *use\s\w*.\w*.all;)', re.I)

# regex expression to get the entity name
regex_entity = re.compile(r'^\s*entity+\s+(\w+)\s+is\s*', re.I)

# regex expression to get all the ports description
# this gets the current data ports organized as:  port_name, direction, type
regex_ports = re.compile(r'^\s*(\w+)\s*\:\s*(in|out|inout|buffer)\s+([[\w| ]*[\(|\)]*[\w| |*|,|-]*[\(|\)]{0,1});*', re.I)

PORT_NAME_ID = 0  # data position in the regex_ports list
PORT_DIR_ID = 1  # data position in the regex_ports list
PORT_TYPE_ID = 2  # data position in the regex_ports list

# specific clock ports
regex_clk = re.compile(r'(\w*clk\w*|\w*clock\w*)', re.I)

# specific reset ports
regex_rst = re.compile(r'(\w*rst\w*|\w*reset\w*)', re.I)

# regex for generics parameters of the architecture
regex_generics = re.compile(r'^\s*(\w*) *: *([\w|_]* *[\d|\w|(|)| |-]*[\w|)]) *:= ([\d|\w|"|.]*) *(\w*)')
GENERIC_NAME_ID = 0     # data position in the regex_generics list
GENERIC_TYPE_ID = 1     # data position in the regex_generics list
GENERIC_VALUE_ID = 2    # data position in the regex_generics list
GENERIC_UNIT_ID = 3     # data position in the regex_generics list

# regex for architectures names
regex_arch = re.compile(r'^\s*architecture (\w*) of', re.I)

default_libraries = "library ieee;\n\tuse ieee.std_logic_1164.all;\n\tuse ieee.numeric_std.all;"


def test_regex(line):
    """
    dummy function to test the regex
    :param line:
    :return:
    """
    regex = re.compile(r'\s*(\w+)\s*\:\s*(in|out|inout)\s*([\w|\s]*).*', re.I)
    result = regex.findall(line)

    if result:
        print(result[0])


def generate_test_bench(file_path):
    """
    Main function to generate a testbench from a VHDL source file. The script takes the input path of the file and
    generates a new file in that directory with a prefix defined by testbench_prefix.
    :param file_path: path to the .vhd file
    :return: nothing
    """

    output_file_path = get_output_file_path(file_path)
    # print(output_file_path)

    testbench_metadata = dict()
    testbench_metadata["header_description"] = list()
    testbench_metadata["libraries"] = list()
    testbench_metadata["entity_name"] = ""
    testbench_metadata["generics"] = list()
    testbench_metadata["ports"] = list()
    testbench_metadata["archs"] = list()

    with open(file_path) as fd:
        entity_name = None
        header_description = list()
        libraries = list()

        data_generics = list()
        data_ports = list()
        arch_names = list()

        entity_complete = False

        for line in fd:

            if entity_name is None:
                # look for header
                result = regex_header.findall(line)
                if result:
                    header_description.append(result[0])

                # look for libraries
                result = regex_libraries.findall(line)
                if result:
                    libraries.append(result[0])

                # look for entity name
                result = regex_entity.findall(line)

                if result:
                    entity_name = result[0]

            if entity_name and not entity_complete:

                # generics:
                result = regex_generics.findall(line)
                result = list(result[0]) if result else None

                if result:
                    data_generics.append(result)

                # ports:
                # result = regex_ports.findall(line.lower())
                result = regex_ports.findall(line)
                result = list(result[0]) if result else None

                if result:
                    data_ports.append(result)

                # end of the entity description
                if ("end " + entity_name in line) or ("end entity" in line):
                    entity_complete = True

            if entity_complete:
                # architecture name
                result = regex_arch.findall(line)
                result = result[0] if result else None

                if result:
                    arch_names.append(result)

        testbench_metadata["header_description"] = header_description
        testbench_metadata["libraries"] = libraries
        testbench_metadata["entity_name"] = entity_name
        testbench_metadata["generics"] = data_generics
        testbench_metadata["ports"] = data_ports
        testbench_metadata["archs"] = arch_names

        write_testbench(output_file_path, testbench_metadata)


def get_output_file_path(file_path):
    """

    :param file_path:
    :return: output file path of the new file
    """
    output_file_ph = ""

    result = regex_path.findall(file_path)
    result = list(result[0]) if result else None

    args = len(result)

    if args == 2:  # file name + extension file
        output_file_ph = testbench_prefix + result[0] + result[1]
    else:
        if args == 3:  # path + file name + extension file
            output_file_ph = result[0] + testbench_prefix + result[1] + result[2]
        else:
            print("Error: arguments in file path!")

    return output_file_ph


def write_testbench(output_file_path, testbench_metadata):
    """

    :param output_file_path:
    :param testbench_metadata: dictionary of the main VHDL module info
        testbench_metadata["entity_name"]: entity name of the selected design
        testbench_metadata["generics"]: list of generics
        testbench_metadata["ports"]: list of ports
        testbench_metadata["header_description"]: header description of the file
        testbench_metadata["libraries"]: libraries used
    :return: nothing
    """

    header = testbench_metadata["header_description"]
    libraries = testbench_metadata["libraries"]

    with open(output_file_path, "w") as fd_o:
        for line in header:
            fd_o.write(line + '\n')

        if libraries:
            for line in libraries:
                fd_o.write(line + '\n')
        else:
            fd_o.write(default_libraries)
            fd_o.write('\n')
        fd_o.write('\n')

        str_body = set_body(testbench_metadata)

        for line in str_body:
            fd_o.write(line)


def set_body(testbench_metadata):
    """
    This is the main function that will write al the testbench code.

    :param testbench_metadata: dictionary of the main VHDL module info
        testbench_metadata["entity_name"]: entity name of the selected design
        testbench_metadata["generics"]: list of generics
        testbench_metadata["ports"]: list of ports
        testbench_metadata["header_description"]: header description of the file
        testbench_metadata["libraries"]: libraries used
    :return: string
    """
    entity_name = testbench_metadata["entity_name"]
    generics_data = testbench_metadata["generics"]
    port_data = testbench_metadata["ports"]

    ports_in = list()
    ports_out = list()
    ports_inout = list()
    ports_buffer = list()

    clk_port_name = "clk"
    rst_port_name = "rst_n"

    clk_port_present = False
    rst_port_present = False

    for port in port_data:
        if port[PORT_DIR_ID] == "in":
            ports_in.append(port)

        if port[PORT_DIR_ID] == "buffer":
            ports_buffer.append(port)

        if port[PORT_DIR_ID] == "inout":
            ports_inout.append(port)

        if port[PORT_DIR_ID] == "out":
            ports_out.append(port)

    n_ports = len(port_data)
    n_generics = len(generics_data)

    # entity of the current testbench declaration
    str_body = """entity tb_""" + entity_name + " is\n"

    if generics_data:
        str_body += "\tgeneric (\n"
        generic_cnt = 0

        for generic in generics_data:
            generic_cnt += 1
            str_body += "\t\t" + generic[GENERIC_NAME_ID] + " : " + generic[GENERIC_TYPE_ID] + " := "
            str_body += generic[GENERIC_VALUE_ID]
            if generic[GENERIC_UNIT_ID]:
                str_body += " " + generic[GENERIC_UNIT_ID]
            if generic_cnt < n_generics:
                str_body += ";\n"
        str_body += "\n\t);\n"

    str_body += "end tb_" + entity_name + ";\n\n"

    # architecture of the testbench ---------------------------------------------------------------------------
    str_body += "architecture behavioral of tb_" + entity_name + """ is

    -- component declarations
    component """ + entity_name + "\n"

    if generics_data:
        str_body += "\tgeneric (\n"
        generic_cnt = 0

        for generic in generics_data:
            generic_cnt += 1
            str_body += "\t\t" + generic[GENERIC_NAME_ID] + " : " + generic[GENERIC_TYPE_ID]
            str_body += " := " + generic[GENERIC_VALUE_ID]
            if generic[GENERIC_UNIT_ID]:
                str_body += " " + generic[GENERIC_UNIT_ID]
            if generic_cnt < n_generics:
                str_body += ";\n"
            else:
                str_body += "\n"
        str_body += "\t);\n"

    str_body += "\tport(\n"""

    # ports declarations
    port_ctr = 0

    if ports_in:
        str_body += "\t\t-- input ports\n"
        for port in ports_in:
            str_body += "\t\t" + port[PORT_NAME_ID] + "\t\t: " + port[PORT_DIR_ID] + "\t" + port[PORT_TYPE_ID]
            port_ctr += 1
            if port_ctr < n_ports:
                str_body += ';\n'
            else:
                str_body += '\n'

    if ports_buffer:
        str_body += "\t\t-- buffer ports\n"
        for port in ports_buffer:
            str_body += "\t\t" + port[PORT_NAME_ID] + "\t\t: " + port[PORT_DIR_ID] + "\t" + port[PORT_TYPE_ID]
            port_ctr += 1
            if port_ctr < n_ports:
                str_body += ';\n'
            else:
                str_body += '\n'

    if ports_inout:
        str_body += "\t\t-- inout ports\n"
        for port in ports_inout:
            str_body += "\t\t" + port[PORT_NAME_ID] + "\t\t: " + port[PORT_DIR_ID] + "\t" + port[PORT_TYPE_ID]
            port_ctr += 1
            if port_ctr < n_ports:
                str_body += ';\n'
            else:
                str_body += '\n'

    if ports_out:
        str_body += "\t\t-- output ports\n"
        for port in ports_out:
            str_body += "\t\t" + port[PORT_NAME_ID] + "\t\t: " + port[PORT_DIR_ID] + "\t" + port[PORT_TYPE_ID]
            port_ctr += 1
            if port_ctr < n_ports:
                str_body += ';\n'
            else:
                str_body += '\n'

    str_body += """\t);
    end component;

    -- clock period definition
    constant c_CLK_PERIOD : time := 10 ns;

    """

    # signals declarations -----------------------------
    str_body += "-- input signals\n"

    # signal s_clk    : std_logic := '0';
    # signal s_rst_n  : std_logic := '0';\n"""

    # writing all the signals to connect to the current module
    module_signals_body = ""

    if ports_in:
        for port in ports_in:

            result = regex_clk.findall(port[PORT_NAME_ID])
            if result and not clk_port_present:
                clk_port_present = True
                clk_port_name = result[0]

            result = regex_rst.findall(port[PORT_NAME_ID])
            if result and not rst_port_present:
                rst_port_present = True
                rst_port_name = result[0]

            module_signals_body += "\tsignal s_" + port[PORT_NAME_ID] + "\t\t: " + port[PORT_TYPE_ID] + ';\n'

    if ports_buffer:
        module_signals_body += "\n\t-- buffer signals\n"
        for port in ports_buffer:
            module_signals_body += "\tsignal s_" + port[PORT_NAME_ID] + "\t\t: " + port[PORT_TYPE_ID] + ';\n'

    if ports_inout:
        module_signals_body += "\n\t-- inout signals\n"
        for port in ports_inout:
            module_signals_body += "\tsignal s_" + port[PORT_NAME_ID] + "\t\t: " + port[PORT_TYPE_ID] + ';\n'

    if ports_out:
        module_signals_body += "\n\t-- output signals\n"
        for port in ports_out:
            module_signals_body += "\tsignal s_" + port[PORT_NAME_ID] + "\t\t: " + port[PORT_TYPE_ID] + ';\n'

    # if clock o reset signal are not present, then it will be included
    if not clk_port_present:
        str_body += "\tsignal s_clk\t: std_logic := '0';\n"

    if not rst_port_present:
        str_body += "\tsignal s_rst_n\t: std_logic := '0';\n"

    # adding now all the signals detected
    str_body += module_signals_body + "\n"

    str_body += "begin\n"

    str_body += "\t-- instantiation of the Unit under test\n"
    str_body += "\tuut : entity work." + entity_name + "(" + testbench_metadata["archs"][0] + ")\n"

    if generics_data:
        str_body += "\tgeneric map(\n"
        generic_cnt = 0

        for generic in generics_data:
            generic_cnt += 1
            str_body += "\t\t" + generic[GENERIC_NAME_ID] + " => " + generic[GENERIC_NAME_ID]

            if generic_cnt < n_generics:
                str_body += ",\n"
            else:
                str_body += "\n"
        str_body += "\t)\n"

    str_body += "\tport map("

    #  -----------------------------------------
    #  entity instantiation

    # signals declarations -----------------------------
    port_ctr = 0

    if ports_in:
        str_body += "\n\t\t-- input ports\n"
        for port in ports_in:
            str_body += "\t\t" + port[0] + "\t=> " + "s_" + port[0]
            port_ctr += 1
            if port_ctr < n_ports:
                str_body += ',\n'
            else:
                str_body += '\n'

    if ports_buffer:
        str_body += "\t\t-- buffer ports\n"
        for port in ports_buffer:
            str_body += "\t\t" + port[0] + "\t=> " + "s_" + port[0]
            port_ctr += 1
            if port_ctr < n_ports:
                str_body += ',\n'
            else:
                str_body += '\n'

    if ports_inout:
        str_body += "\t\t-- inout ports\n"
        for port in ports_inout:
            str_body += "\t\t" + port[0] + "\t=> " + "s_" + port[0]
            port_ctr += 1
            if port_ctr < n_ports:
                str_body += ',\n'
            else:
                str_body += '\n'

    if ports_out:
        str_body += "\t\t-- output ports\n"
        for port in ports_out:
            str_body += "\t\t" + port[0] + "\t=> " + "s_" + port[0]
            port_ctr += 1
            if port_ctr < n_ports:
                str_body += ',\n'
            else:
                str_body += '\n'

    str_body += "\t);\n\n"

    clk_stimulus = """\t-- Clock process definitions
    p_clk_process : process
    begin
        <clock_signal> <= '0';
        wait for c_CLK_PERIOD/2;
        <clock_signal> <= '1';
        wait for c_CLK_PERIOD/2;
    end process;\n"""

    clk_stimulus = clk_stimulus.replace("<clock_signal>", "s_" + clk_port_name)

    process_stimulus = """\n\t-- stimulus process
    p_stim : process
    begin
        <reset_signal> <= '0';
        wait for 40 ns;
        <reset_signal> <= '1';

        wait for c_CLK_PERIOD;

        -- add code here

        -- nothing else to do..
        wait for 3 * c_CLK_PERIOD;

        report "[msg] Testbench end." severity failure ;
    end process;


    end behavioral;
    """
    process_stimulus = process_stimulus.replace("<reset_signal>", "s_" + rst_port_name)

    str_body += clk_stimulus
    str_body += process_stimulus

    return str_body


if __name__ == '__main__':
    """
    main function
    """

    if len(sys.argv) == 2:
        path_to_file = sys.argv[1]
        generate_test_bench(path_to_file)

        print("Script executed successfully")

    elif len(sys.argv) == 3 and sys.argv[2] == "debug":
        path_to_file = sys.argv[1]
        generate_test_bench(path_to_file + ".vhd")

    else:
        print("Incorrect number of arguments")
        print('help: python generate_test_bench sample.vhd')
