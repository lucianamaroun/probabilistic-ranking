# STABILITY
require(ggplot2)
require(scales)
stab <- read.csv('~/probabilistic-ranking/gen/stability10.csv', header=F)
rep <- 10
n <- rep * (rep - 1) / 2 # rethink that
iter <- c(1, 2, 5, 10, 22, 46, 100, 215, 464, 1000)
means <- rep(0, 10)
sds <- rep(0, 10)
colnames(stab) <- c('iter', 'score')
for (i in 1:10) {
  it <- iter[i]
  means[i] <- mean(stab[stab$iter==it,]$score)
  sds[i] <- sd(stab[stab$iter==it,]$score)
}
error <- qnorm(0.975)*sds/sqrt(n)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(iter, means, ci_min, ci_max)
Sys.setlocale("LC_ALL", 'en_US.UTF-8')
ggplot(data, aes(x=iter, y=means), log10='x') + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=.1) + geom_point(size=4, shape=21, fill='white') +  xlab('# Iterações Estocásticas') + ylab('Estabilidade') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=18), axis.title=element_text(size=18)) + scale_x_log10(breaks=10**(0:3), labels=trans_format("log10", math_format(10^.x))) + coord_cartesian(ylim = c(0,0.95)) + scale_y_continuous(breaks=seq(0.1, 0.9, 0.1))

# PAIRWISE STABILITY
require(ggplot2)
require(scales)
stab <- read.csv('~/probabilistic-ranking/gen/stability10-pairwise.csv', header=F)
n <- 10
iter <- c(1, 2, 5, 10, 22, 46, 100, 215, 464, 1000)
means <- rep(0, 10)
sds <- rep(0, 10)
colnames(stab) <- c('iter', 'score')
for (i in 1:10) {
  it <- iter[i]
  means[i] <- mean(stab[stab$iter==it,]$score)
  sds[i] <- sd(stab[stab$iter==it,]$score)
}
error <- qt(0.975,n-1)*sds/sqrt(n)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(iter, means, ci_min, ci_max)
Sys.setlocale("LC_ALL", 'en_US.UTF-8')
ggplot(data, aes(x=iter, y=means), log10='x') + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=.1) + geom_point(size=4, shape=21, fill='white') +  xlab('# Iterações Estocásticas') + ylab('Estabilidade') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=18), axis.title=element_text(size=18)) + scale_x_log10(breaks=10**(0:3), labels=trans_format("log10", math_format(10^.x))) + coord_cartesian(ylim = c(0,0.95)) + scale_y_continuous(breaks=seq(0.1, 0.9, 0.1))
