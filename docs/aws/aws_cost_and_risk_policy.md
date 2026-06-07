# AWS Cost and Risk Policy

## Purpose

This document defines AWS cost and operational risk controls for the Mini SILS/HILS PoC.

The objective is to prevent unexpected charges and unnecessary resource consumption.

This PoC uses personal resources and follows a low-cost approach.

## Cost Control Principles

### Free Tier First

AWS Free Tier shall be used whenever possible.

Paid services shall not be enabled without understanding the expected cost.

### Smallest Practical Configuration

Use the smallest practical resource size for learning activities.

Large-scale environments are out of scope.

### Short Execution Duration

Resources shall run only when required.

Resources shall be stopped or removed after use.

## Resource Review Checklist

Before creating resources:

- confirm Free Tier eligibility
- estimate expected usage
- review storage requirements

Before ending a session:

- stop EC2 instances
- review EBS volumes
- review S3 storage
- review public IP allocations

## Security Principles

### Least Privilege

IAM users and roles should have only the permissions required.

### No Production Data

No company data, customer data, or confidential information shall be uploaded.

Only fictional and general-purpose data may be used.

### Personal Learning Environment

This AWS environment is used only for personal learning and PoC activities.

## Initial AWS Scope

Included:

- Amazon EC2 (Elastic Compute Cloud)
- Amazon S3 (Simple Storage Service)
- IAM (Identity and Access Management)
- Amazon CloudWatch

Excluded:

- Production workloads
- Customer projects
- Corporate environments

## Success Criteria

The AWS phase is successful when:

- costs remain controlled
- resources remain understandable
- mini SILS can be executed safely

