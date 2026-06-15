# trade settlement reconciliation - r statistical analysis

# packages
if ((!require(ggplot2))) install.packages("ggplot2")
if ((!require(dplyr))) install.packages("dplyr")
if ((!require(scales))) install.packages("scales")


library(ggplot2)
library(dplyr)
library(scales)

# load data

breaks <- read.csv("breaks_identified.csv")
trade <- read.csv("trade_data.csv")

cat("==================================================\n")
cat("R STATISTICAL ANALYSIS - BREAK DATA\n")
cat("==================================================\n")
cat("total breaks loaded:", nrow(breaks), "\n")
cat("total trade loaded:", nrow(trade), "\n")

# analysis 1 - basic descriptive statistics
cat("==================================================\n")
cat("DESCRIPTIVE STATISTICS - BREAK AMOUNTS \n")
cat("==================================================\n")

cat("mean break amount :", round(mean(breaks$abs_break_amount), 2), "\n")
cat("median break amount :", round(median(breaks$abs_break_amount), 2), "\n")
cat("std deviation :", round(sd(breaks$abs_break_amount), 2), "\n")
cat("min break  :", round(min(breaks$abs_break_amount), 2), "\n")
cat("max break :", round(max(breaks$abs_break_amount), 2), "\n")
cat("total cash at risk :", round(sum(breaks$abs_break_amount), 2), "\n")


# analysis 2 - risk level breakdown
cat("==================================================\n")
cat("DESCRIPTIVE STATISTICS - BREAK AMOUNTS \n")
cat("==================================================\n")

risk_summary <- breaks |>
  group_by(risk_level) |>
  summarise(
    count = n(),
    total_cash = round(sum(abs_break_amount), 2),
    avg_break = round(mean(abs_break_amount), 2)
  ) |>
  arrange(desc(total_cash))

print(risk_summary)

# analysis 3 counterparty risk ranking
cat("==================================================\n")
cat("COUNTERPARTY RISK RANKING \n")
cat("==================================================\n")

counterparty_summary <- breaks |>
  group_by(counterparty) |>
  summarise(
    total_breaks = n(),
    total_cash_at_risk = round(sum(abs_break_amount), 2),
    avg_break = round(mean(abs_break_amount), 2)
  ) |>
  arrange(desc(total_cash_at_risk))
print(counterparty_summary)

# analysis 4 break direction analysis

cat("==================================================\n")
cat("break direction analysis \n")
cat("==================================================\n")

direction_summary <- breaks |>
  group_by(break_direction) |>
  summarise(
    count = n(),
    total_cash = round(sum(abs_break_amount), 2),
    avg_break = round(mean(abs_break_amount), 2)
  )
print(direction_summary)

# analysis 5 - currency exposure

cat("==================================================\n")
cat("CURRENCY EXPOSURE \n")
cat("==================================================\n")

currency_summary <- breaks |>
  group_by(currency) |>
  summarise(
    total_breaks = n(),
    total_cash_at_risk = round(sum(abs_break_amount), 2)
  ) |>
  arrange(desc(total_cash_at_risk))
print(currency_summary)

# chart 1 - break amount distribution

png("chart1_break_distribution.png", width = 800, height = 500, type = "cairo")
print(
  ggplot(breaks, aes(x = abs_break_amount)) +
    geom_histogram(bins = 50, fill = "#003366", color = "white") +
    scale_x_continuous(labels = comma) +
    labs(
      title = "Distribution of Break Amounts",
      x = "Break Amount",
      y = "Frequency"
    ) +
    theme_minimal()
)
dev.off()
cat("\nchart 1 saved: chart1_break_distribution.png\n")

# chart 2 -cash at risk by counterparty

png("chart2_counterparty_risk.png", width = 800, height = 500, type = "cairo")
print(
  ggplot(counterparty_summary,
         aes(x = reorder(counterparty, total_cash_at_risk),
             y = total_cash_at_risk)) +
    geom_bar(stat = "identity", fill = "#003366") +
    coord_flip() +
    scale_y_continuous(labels = comma) +
    labs(
      title = "Total Cash At Risk by Counterparty",
      x = "Counterparty",
      y = "Total Cash At Risk"
    ) +
    theme_minimal()
)
dev.off()
cat("\nchart 2 saved: chart2_counterparty_risk.png\n")

# chart 3 risk level distribution
png("chart3_risk_distribution.png", width = 800, height = 500, type = "cairo")
print(
  ggplot(breaks, aes(x = risk_level, fill = risk_level)) +
    geom_bar() +
    scale_fill_manual(values = c(
      "high" = "#FF4444",
      "medium" = "#FFA500",
      "low" = "#00AA00"
    )) +
    labs(
      title = "Break Count By Risk Level",
      x = "Risk Level",
      y = "Number of Breaks"
    ) +
    theme_minimal()
)
dev.off()
cat(("chart 3 saved : chart3_risk_distribution.png\n"))

cat("==================================================\n")
cat("R ANALYSIS COMPLETE \n")
cat("3 charts saved as PNG files\n")
cat("==================================================\n")
