---
layout: post
title: test post
tags: reflecting
---


{% if jekyll.environment == "production" %}
   PROD
{% endif %}

{% if jekyll.environment == "development" %}
   DEV
{% endif %}