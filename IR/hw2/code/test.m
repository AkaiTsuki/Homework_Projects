text = textread('output', '%s');
vocabulary = unique(text);
vocabularyLength = length(vocabulary);

dictionary = zeros(1,vocabularyLength);

for i=1:vocabularyLength
    word = vocabulary(i);
    dictionary(i) =sum(strcmp(text,word));
end

sortedList = sort(dictionary,'descend');
h= loglog(sortedList, 'o');
xlabel('rank');
ylabel('# of ocurances');
saveas(h, 'ordered_words.fig');
saveas(h, 'ordered_words.jpg');