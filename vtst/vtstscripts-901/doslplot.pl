#!/usr/bin/env perl
#;-*- Perl -*-

@ARGV>0 || die "usage: doslplot.pl <s,p,d,a=(all)> <atom num(s)>\n";

open (DOS,"DOS1");
<DOS>;
$in = <DOS>;
$in =~ s/^\s+//g;
@line = split(/\s+/,$in);
$spin = @line;

if($spin == 4) { np_plot(); }
if($spin == 7) { sp_plot(); }

# Subroutine for non-polarized
sub np_plot{
    # If no orbital flag, plot the d-band
    $col = 4;
    if(@ARGV>0) {
        $arg1 = @ARGV[0];
        if($arg1 =~ /^\d+$/) {
        } else {
            $oflag = shift(@ARGV);
            if($oflag eq 's') { $col = 2; }
            if($oflag eq 'p') { $col = 3; }
            if($oflag eq 'd') { $col = 4; }
            if($oflag eq 'a') { $col = 5; } # plot s+p+d
        }
    }

    # Set selected atom(s)
    ## $NumAtm=@ARGV;
    ## @Atm=@ARGV;
    if(@ARGV[0] =~ /^\d+$/) {
        $NumAtm = @ARGV;
        @Atm = @ARGV;
    } elsif(@ARGV[0] =~ /^(\d+)(-)(\d+)$/) {
        $NumAtm = $3 - $1+1;
        for($i=0; $i<$NumAtm; $i++) {
            $Atm[$i] = $i+$1;
        }
    }

    $gnufile = "ldosplot.gnu";
    $epsfile = "ldosplot.eps";

    open GNUPLOT, ">$gnufile";
    print GNUPLOT "set grid\n";
    print GNUPLOT "set pointsize 2\n";
    print GNUPLOT "set xlabel \"Energy [eV]\"\n";
    print GNUPLOT "set ylabel \"DOS\"\n";
    print GNUPLOT "set nokey\n";
    print GNUPLOT "set terminal postscript eps color\n";
    print GNUPLOT "set output \"$epsfile\"\n";

    # Find how many atom DOS there are
    opendir MAINDIR, "." or die "can't open this dir!" ;
    @DOSFILE = grep /^DOS\d+$/, readdir MAINDIR ;
    $NumDOS = @DOSFILE;
    closedir MAINDIR ;
    print GNUPLOT "plot ";

     # If no atom is selected, plot all of them
    if($NumAtm==0) {
        $NumPlot = $NumDOS-1;
    } else {
        $NumPlot = $NumAtm;
    }

    # Write plot data to a gnuplot script file
    for ($i=1; $i<=$NumPlot; $i++) {
        if($NumAtm == 0) {
            $DOSFILE = "DOS"."$i";
        } else {
            $a = $Atm[$i-1];
            $DOSFILE = "DOS"."$a";
        }
        print GNUPLOT "   \"$DOSFILE\" u 1:";
        if($col == 5) {
            print GNUPLOT "((\$2+\$3+\$4)*$NumDOS)";
        } else {
            print GNUPLOT "(\$$col*$NumDOS)";
        }
        print GNUPLOT " w l lt 3 lw 2.0,\\\n";
    }
    print GNUPLOT "   \"DOS0\" u 1:2 w lp lt 1 lw 2.0 pt 7 ps 0.4\n";
    close GNUPLOT;

    # Plot graphs with gnuplot and show with ghostview
    system("gnuplot < $gnufile");
    #system("gv -scale 2 $epsfile \&");
    system("rm $gnufile");
# End of subroutine np_plot
}

# Subroutine for spin-polarized
sub sp_plot{
    #If no orbital flag, plot the d-band
    $col = 4;
    if(@ARGV > 0) {
        $arg1 = @ARGV[0];
        if($arg1 =~ /^\d+$/) {
        } else {
            $oflag = shift(@ARGV);
            if($oflag eq 's') { $col = 2; $col2 = $col+1; }
            if($oflag eq 'p') { $col = 4; $col2 = $col+1; }
            if($oflag eq 'd') { $col = 6; $col2 = $col+1; }
            if($oflag eq 'a') { $col = 8; } # plot s+p+d
        }
    }

    # Set selected atom(s)
    ## $NumAtm=@ARGV;
    ## @Atm=@ARGV;
    if(@ARGV[0] =~ /^\d+$/) {
        $NumAtm = @ARGV;
        @Atm = @ARGV;
    } elsif(@ARGV[0] =~ /^(\d+)(-)(\d+)$/) {
        $NumAtm = $3 - $1+1;
        for($i=0; $i<$NumAtm; $i++){
            $Atm[$i] = $i+$1;
        }
    }

    $gnufile = "ldosplot.gnu";
    $epsfile = "ldosplot.eps";

    open GNUPLOT, ">$gnufile";
    print GNUPLOT "set grid\n";
    print GNUPLOT "set pointsize 2\n";
    print GNUPLOT "set xlabel \"Energy [eV]\"\n";
    print GNUPLOT "set ylabel \"DOS\"\n";
    print GNUPLOT "set nokey\n";
    print GNUPLOT "set terminal postscript eps color\n";
    print GNUPLOT "set output \"$epsfile\"\n";

    # Find how many atom DOS there are
    opendir MAINDIR, "." or die "can't open this dir!" ;
    @DOSFILE = grep /^DOS\d+$/, readdir MAINDIR ;
    $NumDOS = @DOSFILE;
    closedir MAINDIR ;
    print GNUPLOT "plot ";

    # If no atom is selected, plot all of them
    if($NumAtm == 0) {
        $NumPlot = $NumDOS-1;
    } else {
        $NumPlot = $NumAtm;
    }

    # Write plot data to a gnuplot script file
    for ($i=1; $i<=$NumPlot; $i++) {
        if($NumAtm == 0) {
            $DOSFILE = "DOS"."$i";
        } else {
            $a = $Atm[$i-1];
            $DOSFILE = "DOS"."$a";
        }
        print GNUPLOT "   \"$DOSFILE\" u 1:";
        if($col == 8) {
            print GNUPLOT "((\$2-\$3+\$4-\$5+\$6-\$7)*$NumDOS)";
        } else {
            print GNUPLOT "((\$$col-\$$col2)*$NumDOS)";
        }
        print GNUPLOT " w l lt 3 lw 2.0,\\\n";
    }
    print GNUPLOT "   \"DOS0\" u 1:2 w lp lt 1 lw 2.0 pt 7 ps 0.4\n";
    close GNUPLOT;

    # Plot graphs with gnuplot and show with ghostview
    system("gnuplot < $gnufile");
    #system("gv -scale 2 $epsfile \&");
    system("rm $gnufile");
    #End of subroutine
}
