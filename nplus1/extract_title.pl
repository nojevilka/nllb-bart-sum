my $path = $ARGV[0];
my $input = `cat $path`;

while ($input =~ /<h1.*?>(.*)<\/h1>/gs) {
    $v = $1;
    $v =~ s/^\s+|\s+$//g;
    print $v;
}
