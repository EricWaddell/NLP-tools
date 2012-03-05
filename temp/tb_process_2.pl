#!/usr/local/bin/perl

# Noah Smith
# 3-16-08
# Reads in raw treebank trees (standard input), 
# writes out each rule as it's encountered (standard output).
#
# Intended as a starter script for doing more interesting treebank
# processing tasks.

$ROOT_symbol = 'ROOT';

$line = <>;
do {
    $x = $line;
    while($line = <> and $line =~ m/^ /) {
	$x .= $line;
    } 
    $x =~ s/\n/ /g;
    $x =~ s/\#/<HASH>/g; # because some tools treat # as a comment character
    recursive_descent($x) if($line =~ m/\S/);
} while($line ne "");

# depth-first processing of treebank trees in their usual LISP format
sub recursive_descent {
    my $line = shift;
    my($y, $z, $lhs);
    my(@rhs);
    if($line =~ m/^\(/) {
	($lhs, $z) = ($line =~ m/^\(([^\(\)\ ]*)\s+(.*)$/);
	$lhs = $ROOT_symbol if($lhs eq ''); # insert ROOT as root symbol
	while($z =~ m/^\(/) { # for each child, recur
	    ($y, $z) = recursive_descent($z);
	    push @rhs, $y;
	}
	if($z =~ m/^\)\s*(.*)$/) { # eat the right parenthesis
	    $z = $1;
	}
	else { # this is a preterminal node, we need to grab the terminal
	    die "malformed rule with mix of nonterms and terms on rhs:\n$line" if(scalar(@rhs) > 0);
	    ($y, $z) = ($z =~ m/^([^\)]+)\)\s*(.*)$/);
	    push @rhs, $y;
	}
	$rhs = @rhs;
	if($rhs > 1)'
	{
		$type = "nonterminal";
	}
	else
	{
		$type = "terminal";
	}
	print $type . ": $lhs -> ", (join " ", @rhs), "\n"; # print the rule
	return ($lhs, $z);  # return the label of this node, and any remaining tree
    }
    else {
	die "was expecting (, got:\n$line";
    }
}
