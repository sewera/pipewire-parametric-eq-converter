#!/usr/bin/python3
txt_file = "input.eq.txt" # TODO: Add a parameter to select the input file
output_file = open("output.filter.conf", "a+")

# Beginning of conf
output_file.write('\
context.modules = [ \n\
    { name = libpipewire-module-filter-chain \n\
        args = { \n\
            node.description = "Pipewire Equalizer" \n\
            media.name       = "Pipewire Equalizer" \n\
            filter.graph = { \n\
                nodes = [ \n')

with open(txt_file, "r") as input_file:
    # read first string, useless for now
    string = input_file.readline().strip()

    # LOWSHELF
    output_file.write('\
                    { \n\
                        type  = builtin \n\
                        name  = eq_band_1 \n\
                        label = bq_lowshelf \n')
    # read second string for 'lowshelf'
    string = input_file.readline().strip() # strip is to prevent \n at the end of the line
    output_file.write('\
                        control = { "Freq" = ' + string.split(" ")[5] + ' "Q" = ' + string.split(" ")[11] + ' "Gain" = ' + string.split(" ")[8] + ' }\n\
                    }')

    # PEAKS
    peaks = 8
    # read and write parameters for 'peaks'
    for i in range(peaks):
        string = input_file.readline().strip()
        output_file.write('\n\
                    { \n\
                        type  = builtin \n\
                        name  = eq_band_' + str(i+2) + '\n\
                        label = bq_peaking \n\
                        control = { "Freq" = ' + string.split(" ")[5] + ' "Q" = ' + string.split(" ")[11] + ' "Gain" = ' + string.split(" ")[8] + ' }\n\
                    }')

    # HIGHSHELF
    output_file.write('\n\
                    { \n\
                        type  = builtin \n\
                        name  = eq_band_10 \n\
                        label = bq_highshelf \n')
    # read 10th string for 'highshelf'
    string = input_file.readline().strip() # strip is to prevent \n at the end of the line
    output_file.write('\
                        control = { "Freq" = ' + string.split(" ")[5] + ' "Q" = ' + string.split(" ")[11] + ' "Gain" = ' + string.split(" ")[8] + ' }\n\
                    }')

output_file.write('\n\
                ] \n\
                links = [ \n\
                    { output = "eq_band_1:Out" input = "eq_band_2:In" } \n\
                    { output = "eq_band_2:Out" input = "eq_band_3:In" } \n\
                    { output = "eq_band_3:Out" input = "eq_band_4:In" } \n\
                    { output = "eq_band_4:Out" input = "eq_band_5:In" } \n\
                    { output = "eq_band_5:Out" input = "eq_band_6:In" } \n\
                    { output = "eq_band_6:Out" input = "eq_band_7:In" } \n\
                    { output = "eq_band_7:Out" input = "eq_band_8:In" } \n\
                    { output = "eq_band_8:Out" input = "eq_band_9:In" } \n\
                    { output = "eq_band_9:Out" input = "eq_band_10:In" } \n\
                ] \n\
            } \n\
	    audio.channels = 2 \n\
	    audio.position = [ FL FR ] \n\
            capture.props = { \n\
                node.name   = "effect_input.eq6" \n\
                media.class = Audio/Sink \n\
            } \n\
            playback.props = { \n\
                node.name   = "effect_output.eq6" \n\
                node.passive = true \n\
            } \n\
        } \n\
    } \n\
]')

output_file.close()
input_file.close()
