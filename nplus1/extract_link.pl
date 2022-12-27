my $path = $ARGV[0];
my $input = `cat $path`;

$input =~ /<link rel="canonical" href="(.*)">/;
print $1;
