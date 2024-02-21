# Used iPhone pricing tool

> ## Disclaimer:
> This is only for educational purposes as the source of data is Njuskalo.hr and they do not allow legally scraping data from their website.

### The whole purpose of completing such a project was to test the hypothesis of how data collected from online ads are correlated and if based on data such as 
1. iPhone model 
2. ROM size 
3. Battery health 
4. Warranty status
### can predict the price of a used iPhone.

The only hurdle was the quantity of data. 

As there were only from 50 to 200 ads per iPhone model at a time, collectively amounting to 1300, 1400 ads. Of that number, only half of the ads had valid information on battery health. Managing missing information using different methods such as `mean` didn't contribute to a better result.

Most influential data on price was certainly the model and ROM size.
**Battery health** was slightly positively correlated to the price if each model was observed separately.

Looking at **battery health** as information of all data collectively the correlation was evident because newer iPhone models had better battery health compared to older models and newer models had higher prices. 

### Correlation between Battery Health and Price
![Regression line](/images/battery_price_corr.png)

### Battery Helath information grouped by Model
![](/images/battery_health_distribution.png)

## Linear Regression Model

>**_R^2 score_** on Test data was around **_0.9_** meaning that the most variations can be explained by the model.
> The best R^2 score was obtained using Polynomial Features of the 3rd degree

### Density plot of Train data

![](/images/density_train.png)

### Density plot of Test data

![](/images/density_test.png)

Looking at density plots of actual vs predicted prices based on input information (_model_, _ROM size_ and _battery health_) on Training and Test data the highest discrepancy lies in the range of 350€ and 600€ which is mostly influenced by similar Battery health information among different models

## Conclusion

The prices of used iPhones were mostly determined based on Model and Rom size. Also, a huge influence had a subjective perception of other factors such as the cosmetic condition of particular phone. 

Models prediction of the price based on input information could give an objective estimate of the price range and could help in spotting a good opportunity to buy the used phone and then resell it for a profit