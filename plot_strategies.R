plot_wordle_strategies <- function(plot_number = 1, output_filename = '') {
    # Compute the average of a frequency histogram represented as a vector x, beginning at 1 and having no gaps
    histogram_average <- function(x) {
        sum(seq(length(x)) * x / sum(x))
    }

    if (plot_number == 1) {
        # Examples of one word opening strategies
        tares <- c(0, 8, 482, 1399, 404, 21, 1)
        crane <- c(1, 15, 512, 1327, 427, 32, 1)
        slant <- c(1, 13, 484, 1390, 400, 27, 0)
        print('Averages for: tares, crane, slant')
        print(c(histogram_average(tares), histogram_average(crane), histogram_average(slant)))
        # 3.978834 3.977970 3.974514
        combined <- as.vector(t(cbind(tares, crane, slant)))
        legend_text <- c('tares (avg = 3.979)', 'crane (avg = 3.978)', 'slant (avg = 3.975)')
    }
    else if (plot_number == 2) {
        # Examples of two word opening strategies
        nares_doilt <- c(0, 0, 368, 1407, 509, 31)
        slant_price <- c(1, 1, 406, 1360, 509, 38)
        solid_crate <- c(1, 1, 354, 1374, 541, 44)
        print('Averages for: nares doilt, slant price, solid crate:')
        print(c(histogram_average(nares_doilt), histogram_average(slant_price), histogram_average(solid_crate)))
        # 4.087689 4.075162 4.116631
        combined <- as.vector(t(cbind(nares_doilt, slant_price, solid_crate)))
        legend_text <- c('nares doilt (avg = 4.088)', 'slant price (avg = 4.075)', 'solid crate (avg = 4.117)')
    }

    three_viridis_colors <- c('#3a5e8cFF', '#10a53dFF', '#541352FF')
    if (output_filename != '')
        png(output_filename, width = 800, height = 496)

    barplot(matrix(combined, nr = 3), beside = T, col = three_viridis_colors,
        main = 'Wordle Strategies', names.arg = 1:(length(combined) / 3),
        xlab = 'Number of guesses', ylab = 'Number of answers')
    legend('topleft', legend_text, pch = 15, col = three_viridis_colors)

    if (output_filename != '')
        dev.off()
}
