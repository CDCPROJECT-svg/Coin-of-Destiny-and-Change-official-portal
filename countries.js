// countries.js — 204 Countries + Currency
document.addEventListener("DOMContentLoaded", () => {
  const countrySelect = document.getElementById("countrySelect");
  if (!countrySelect) return;

  const countries = [
    "🪙 CODAC-Coin","💲 USDT",
    "🇦🇫 Afghanistan – AFN","🇦🇱 Albania – ALL","🇩🇿 Algeria – DZD","🇦🇩 Andorra – EUR","🇦🇴 Angola – AOA",
    "🇦🇷 Argentina – ARS","🇦🇲 Armenia – AMD","🇦🇺 Australia – AUD","🇦🇹 Austria – EUR","🇦🇿 Azerbaijan – AZN",
    "🇧🇸 Bahamas – BSD","🇧🇭 Bahrain – BHD","🇧🇩 Bangladesh – BDT","🇧🇧 Barbados – BBD","🇧🇾 Belarus – BYN",
    "🇧🇪 Belgium – EUR","🇧🇿 Belize – BZD","🇧🇯 Benin – XOF","🇧🇹 Bhutan – BTN","🇧🇴 Bolivia – BOB",
    "🇧🇦 Bosnia – BAM","🇧🇼 Botswana – BWP","🇧🇷 Brazil – BRL","🇧🇳 Brunei – BND","🇧🇬 Bulgaria – BGN",
    "🇰🇭 Cambodia – KHR","🇨🇲 Cameroon – XAF","🇨🇦 Canada – CAD","🇨🇱 Chile – CLP","🇨🇳 China – CNY",
    "🇨🇴 Colombia – COP","🇨🇩 Congo – CDF","🇨🇷 Costa Rica – CRC","🇭🇷 Croatia – EUR","🇨🇺 Cuba – CUP",
    "🇨🇾 Cyprus – EUR","🇨🇿 Czech Republic – CZK",
    "🇩🇰 Denmark – DKK","🇩🇴 Dominican Republic – DOP",
    "🇪🇨 Ecuador – USD","🇪🇬 Egypt – EGP","🇸🇻 El Salvador – USD","🇪🇪 Estonia – EUR","🇪🇹 Ethiopia – ETB",
    "🇫🇮 Finland – EUR","🇫🇷 France – EUR",
    "🇬🇪 Georgia – GEL","🇩🇪 Germany – EUR","🇬🇭 Ghana – GHS","🇬🇷 Greece – EUR","🇬🇹 Guatemala – GTQ",
    "🇭🇹 Haiti – HTG","🇭🇳 Honduras – HNL","🇭🇺 Hungary – HUF",
    "🇮🇸 Iceland – ISK","🇮🇳 India – INR","🇮🇩 Indonesia – IDR","🇮🇷 Iran – IRR","🇮🇶 Iraq – IQD",
    "🇮🇪 Ireland – EUR","🇮🇱 Israel – ILS","🇮🇹 Italy – EUR",
    "🇯🇲 Jamaica – JMD","🇯🇵 Japan – JPY","🇯🇴 Jordan – JOD",
    "🇰🇪 Kenya – KES","🇰🇼 Kuwait – KWD",
    "🇱🇦 Laos – LAK","🇱🇻 Latvia – EUR","🇱🇧 Lebanon – LBP","🇱🇹 Lithuania – EUR",
    "🇲🇾 Malaysia – MYR","🇲🇽 Mexico – MXN","🇲🇳 Mongolia – MNT","🇲🇦 Morocco – MAD",
    "🇳🇵 Nepal – NPR","🇳🇱 Netherlands – EUR","🇳🇿 New Zealand – NZD","🇳🇬 Nigeria – NGN",
    "🇰🇵 North Korea – KPW","🇳🇴 Norway – NOK",
    "🇴🇲 Oman – OMR",
    "🇵🇰 Pakistan – PKR","🇵🇦 Panama – USD","🇵🇭 Philippines – PHP","🇵🇱 Poland – PLN",
    "🇵🇹 Portugal – EUR",
    "🇶🇦 Qatar – QAR",
    "🇷🇴 Romania – RON","🇷🇺 Russia – RUB",
    "🇸🇦 Saudi Arabia – SAR","🇸🇬 Singapore – SGD","🇸🇰 Slovakia – EUR","🇸🇮 Slovenia – EUR",
    "🇿🇦 South Africa – ZAR","🇰🇷 South Korea – KRW","🇪🇸 Spain – EUR",
    "🇱🇰 Sri Lanka – LKR","🇸🇪 Sweden – SEK","🇨🇭 Switzerland – CHF",
    "🇹🇼 Taiwan – TWD","🇹🇭 Thailand – THB","🇹🇷 Turkey – TRY",
    "🇺🇦 Ukraine – UAH","🇦🇪 United Arab Emirates – AED",
    "🇬🇧 United Kingdom – GBP","🇺🇸 United States – USD","🇺🇾 Uruguay – UYU",
    "🇻🇳 Vietnam – VND",
    "🇿🇲 Zambia – ZMW","🇿🇼 Zimbabwe – ZWL"
  ];

  countries.forEach(c => {
    const opt = document.createElement("option");
    opt.textContent = c;
    countrySelect.appendChild(opt);
  });
});
