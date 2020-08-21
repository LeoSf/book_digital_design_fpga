# *****************************************************************************************
# Leandro Medus 2020
#
# Tool: Vivado (TM) v2019.1 (64-bit)
#
# auto_generate_project.tcl: Tcl script for creating project
#
# Description:  TBD
#
# This file contains the Vivado Tcl commands for creating a project from the workflow
# template. In order to create the project, please source this file in the Vivado Tcl
# Shell.
#
#
# *****************************************************************************************

# User customization -----------------------------------------------------
# Set the project name
set _xil_proj_name_ "project_template"

# Set the module name
set _xil_module_name_ "module_template"

# Set path to source template
set repo_dir "D:/Repos/FPGA/book_digital_design_fpga"

set _ext "v"
#set _ext "vhd"

# \User customization -----------------------------------------------------

# Set the reference directory for source file relative paths (by default the value is
# script directory path)
set origin_dir "."

variable script_file
set script_file "auto_generate_project.tcl"

# Use origin directory path location variable, if specified in the tcl shell
if { [info exists ::origin_dir_loc] } {
  set origin_dir $::origin_dir_loc
}

# Use project name variable, if specified in the tcl shell
if { [info exists ::user_project_name] } {
  set _xil_proj_name_ $::user_project_name
}

# Help information for this script
proc print_help {} {
  variable script_file
  puts "\nDescription:"
  puts "TCL script to generate a Vivado 2019.1 project based on my template. This"
  puts "select automatically Basys 3 board and create two source files, the new "
  puts "current module under development and its testbench.\n"
  puts "                                                         Leandro Medus \n"
  puts "Syntax:"
  puts "$script_file"
  puts "$script_file -tclargs \[--origin_dir <path>\]"
  puts "$script_file -tclargs \[--project_name <name>\]"
  puts "$script_file -tclargs \[--module_name <name>\]"
  puts "$script_file -tclargs \[--help\]\n"
  puts "Usage:"
  puts "Name                   Description"
  puts "-------------------------------------------------------------------------"
  puts "\[--origin_dir <path>\]  Determine source file paths wrt this path. Default"
  puts "                       origin_dir path value is \".\", otherwise, the value"
  puts "                       that was set with the \"-paths_relative_to\" switch"
  puts "                       when this script was generated.\n"
  puts "\[--project_name <name>\] Create project with the specified name. "
  puts "                       project_template is the name of the project.\n"
  puts "\[--module_name <name>\] Set the name of the main module. By default, the"
  puts "                       script will generate two files module.vhd and "
  puts "                       tb_module.vhd. If the name is set, files will be named"
  puts "                       <name>.vhd and tb_<name>.vhd.\n"
  puts "\[--help\]               Print help information for this script"
  puts "-------------------------------------------------------------------------\n"
  exit 0
}

if { $::argc > 0 } {
  for {set i 0} {$i < $::argc} {incr i} {
    set option [string trim [lindex $::argv $i]]
    switch -regexp -- $option {
      "--origin_dir"   { incr i; set origin_dir [lindex $::argv $i] }
      "--project_name" { incr i; set _xil_proj_name_ [lindex $::argv $i] }
      "--module_name" { incr i; set _xil_module_name_ [lindex $::argv $i] }
      "--help"         { print_help }
      default {
        if { [regexp {^-} $option] } {
          puts "ERROR: Unknown option '$option' specified, please type '$script_file -tclargs --help' for usage info.\n"
          return 1
        }
      }
    }
  }
}

# Create project
create_project ${_xil_proj_name_} ${origin_dir}/${_xil_proj_name_} -part xc7a35tcpg236-1

# Set the directory path for the new project
set proj_dir [get_property directory [current_project]]

# Set project properties
set obj [current_project]
set_property -name "board_part" -value "digilentinc.com:basys3:part0:1.1" -objects $obj
set_property -name "default_lib" -value "xil_defaultlib" -objects $obj
set_property -name "dsa.accelerator_binary_content" -value "bitstream" -objects $obj
set_property -name "dsa.accelerator_binary_format" -value "xclbin2" -objects $obj
set_property -name "dsa.board_id" -value "basys3" -objects $obj
set_property -name "dsa.description" -value "Vivado generated DSA" -objects $obj
set_property -name "dsa.dr_bd_base_address" -value "0" -objects $obj
set_property -name "dsa.emu_dir" -value "emu" -objects $obj
set_property -name "dsa.flash_interface_type" -value "bpix16" -objects $obj
set_property -name "dsa.flash_offset_address" -value "0" -objects $obj
set_property -name "dsa.flash_size" -value "1024" -objects $obj
set_property -name "dsa.host_architecture" -value "x86_64" -objects $obj
set_property -name "dsa.host_interface" -value "pcie" -objects $obj
set_property -name "dsa.num_compute_units" -value "60" -objects $obj
set_property -name "dsa.platform_state" -value "pre_synth" -objects $obj
set_property -name "dsa.vendor" -value "xilinx" -objects $obj
set_property -name "dsa.version" -value "0.0" -objects $obj
set_property -name "enable_vhdl_2008" -value "1" -objects $obj
set_property -name "ip_cache_permissions" -value "read write" -objects $obj
#set_property -name "ip_output_repo" -value "$proj_dir/${_xil_proj_name_}.cache/ip" -objects $obj
set_property -name "ip_output_repo" -value "$proj_dir/ip" -objects $obj
set_property -name "mem.enable_memory_map_generation" -value "1" -objects $obj
set_property -name "sim.central_dir" -value "$proj_dir/${_xil_proj_name_}.ip_user_files" -objects $obj
set_property -name "sim.ip.auto_export_scripts" -value "1" -objects $obj
set_property -name "simulator_language" -value "Mixed" -objects $obj

set_property -name "target_language" -value "VHDL" -objects $obj
set_property -name "xsim.array_display_limit" -value "1024" -objects $obj
set_property -name "xsim.radix" -value "hex" -objects $obj
set_property -name "xsim.time_unit" -value "ns" -objects $obj
set_property -name "xsim.trace_limit" -value "65536" -objects $obj

# create src directory to alocate vhdl files
file mkdir $proj_dir/src ;# [file mkdir] in Tcl is like mkdir -p
#file attributes $proj_dir/src -owner system

file copy $repo_dir/template.$_ext $proj_dir/src/${_xil_module_name_}.${_ext}
file copy $repo_dir/template.$_ext $proj_dir/src/tb_${_xil_module_name_}.${_ext}

# Create 'sources_1' fileset (if not found)
if {[string equal [get_filesets -quiet sources_1] ""]} {
  create_fileset -srcset sources_1
}

#add_files -norecurse "./sub3.vhd"\

# Set 'sources_1' fileset object
set obj [get_filesets sources_1]
# Import local files from the original project
add_files -norecurse $proj_dir/src/${_xil_module_name_}.$_ext

# ----------

# Create 'sim_1' fileset (if not found)
if {[string equal [get_filesets -quiet sim_1] ""]} {
  create_fileset -simset sim_1
}

add_files -norecurse $proj_dir/src/tb_${_xil_module_name_}.$_ext

# Set 'sources_1' fileset object
set obj [get_filesets sources_1]

# Set 'sources_1' fileset file properties for local files
set file "src/${_xil_module_name_}."${_ext}
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property -name "file_type" -value "VHDL" -objects $file_obj
set_property -name "is_enabled" -value "1" -objects $file_obj
set_property -name "is_global_include" -value "0" -objects $file_obj
set_property -name "library" -value "xil_defaultlib" -objects $file_obj
set_property -name "path_mode" -value "RelativeFirst" -objects $file_obj
set_property -name "used_in" -value "synthesis simulation" -objects $file_obj
set_property -name "used_in_simulation" -value "1" -objects $file_obj
set_property -name "used_in_synthesis" -value "1" -objects $file_obj

set file "src/tb_${_xil_module_name_}."${_ext}
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property -name "file_type" -value "VHDL" -objects $file_obj
set_property -name "is_enabled" -value "1" -objects $file_obj
set_property -name "is_global_include" -value "0" -objects $file_obj
set_property -name "library" -value "xil_defaultlib" -objects $file_obj
set_property -name "path_mode" -value "RelativeFirst" -objects $file_obj
set_property -name "used_in" -value "simulation" -objects $file_obj
set_property -name "used_in_simulation" -value "1" -objects $file_obj
set_property -name "used_in_synthesis" -value "0" -objects $file_obj


# Set 'sources_1' fileset properties
set obj [get_filesets sources_1]
set_property -name "design_mode" -value "RTL" -objects $obj
set_property -name "edif_extra_search_paths" -value "" -objects $obj
set_property -name "elab_link_dcps" -value "1" -objects $obj
set_property -name "elab_load_timing_constraints" -value "1" -objects $obj
set_property -name "generic" -value "" -objects $obj
set_property -name "include_dirs" -value "" -objects $obj
set_property -name "lib_map_file" -value "" -objects $obj
set_property -name "loop_count" -value "1000" -objects $obj
set_property -name "name" -value "sources_1" -objects $obj
set_property -name "top" -value "${_xil_module_name_}" -objects $obj
set_property -name "top_auto_set" -value "0" -objects $obj
set_property -name "verilog_define" -value "" -objects $obj
set_property -name "verilog_uppercase" -value "0" -objects $obj
set_property -name "verilog_version" -value "verilog_2001" -objects $obj
set_property -name "vhdl_version" -value "vhdl_2k" -objects $obj


# Set 'sim_1' fileset object
set obj [get_filesets sim_1]
# Empty (no sources present)

# Set 'sim_1' fileset properties
set obj [get_filesets sim_1]
set_property -name "32bit" -value "0" -objects $obj
set_property -name "generic" -value "" -objects $obj
set_property -name "include_dirs" -value "" -objects $obj
set_property -name "incremental" -value "1" -objects $obj
set_property -name "name" -value "sim_1" -objects $obj
set_property -name "nl.cell" -value "" -objects $obj
set_property -name "nl.incl_unisim_models" -value "0" -objects $obj
set_property -name "nl.process_corner" -value "slow" -objects $obj
set_property -name "nl.rename_top" -value "" -objects $obj
set_property -name "nl.sdf_anno" -value "1" -objects $obj
set_property -name "nl.write_all_overrides" -value "0" -objects $obj
set_property -name "source_set" -value "sources_1" -objects $obj
set_property -name "systemc_include_dirs" -value "" -objects $obj
set_property -name "top" -value "tb_${_xil_module_name_}" -objects $obj
set_property -name "top_lib" -value "xil_defaultlib" -objects $obj
set_property -name "transport_int_delay" -value "0" -objects $obj
set_property -name "transport_path_delay" -value "0" -objects $obj
set_property -name "verilog_define" -value "" -objects $obj
set_property -name "verilog_uppercase" -value "0" -objects $obj
set_property -name "xelab.dll" -value "0" -objects $obj
set_property -name "xsim.compile.tcl.pre" -value "" -objects $obj
set_property -name "xsim.compile.xsc.more_options" -value "" -objects $obj
set_property -name "xsim.compile.xvhdl.more_options" -value "" -objects $obj
set_property -name "xsim.compile.xvhdl.nosort" -value "1" -objects $obj
set_property -name "xsim.compile.xvhdl.relax" -value "1" -objects $obj
set_property -name "xsim.compile.xvlog.more_options" -value "" -objects $obj
set_property -name "xsim.compile.xvlog.nosort" -value "1" -objects $obj
set_property -name "xsim.compile.xvlog.relax" -value "1" -objects $obj
set_property -name "xsim.elaborate.debug_level" -value "typical" -objects $obj
set_property -name "xsim.elaborate.load_glbl" -value "1" -objects $obj
set_property -name "xsim.elaborate.mt_level" -value "auto" -objects $obj
set_property -name "xsim.elaborate.rangecheck" -value "0" -objects $obj
set_property -name "xsim.elaborate.relax" -value "1" -objects $obj
set_property -name "xsim.elaborate.sdf_delay" -value "sdfmax" -objects $obj
set_property -name "xsim.elaborate.snapshot" -value "" -objects $obj
set_property -name "xsim.elaborate.xelab.more_options" -value "" -objects $obj
set_property -name "xsim.elaborate.xsc.more_options" -value "" -objects $obj
set_property -name "xsim.simulate.add_positional" -value "0" -objects $obj
set_property -name "xsim.simulate.custom_tcl" -value "" -objects $obj
set_property -name "xsim.simulate.log_all_signals" -value "0" -objects $obj
set_property -name "xsim.simulate.no_quit" -value "0" -objects $obj
set_property -name "xsim.simulate.runtime" -value "1000ns" -objects $obj
set_property -name "xsim.simulate.saif" -value "" -objects $obj
set_property -name "xsim.simulate.saif_all_signals" -value "0" -objects $obj
set_property -name "xsim.simulate.saif_scope" -value "" -objects $obj
set_property -name "xsim.simulate.tcl.post" -value "" -objects $obj
set_property -name "xsim.simulate.wdb" -value "" -objects $obj
set_property -name "xsim.simulate.xsim.more_options" -value "" -objects $obj


## Delete previous logs and journals
file delete {*}[glob vivado*.backup.jou]
file delete {*}[glob vivado*.backup.log]
file delete -force .Xil/
