my $input = `cat all_pages_html`;

while ($input =~ /"(https:\/\/nplus1\.ru\/news.*?|https:\/\/vk\.cc\/......)"/g) {
    print $1;
}
